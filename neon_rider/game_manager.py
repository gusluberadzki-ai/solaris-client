# game_manager.py - Core game logic and state management

import math
import pygame
from settings import *
from physics import Bike
from terrain import Terrain
from camera import Camera
from particles import ParticleEmitter
from ui import UI

class GameManager:
    """Manages overall game state and logic."""
    
    def __init__(self, surface):
        self.surface = surface
        self.state = "menu"  # "menu", "playing", "game_over"
        self.score = 0
        self.high_score = 0
        self.multiplier = 1.0
        self.distance_traveled = 0
        self.last_position = 0
        self.game_time = 0
        
        # Game objects
        self.bike = None
        self.terrain = None
        self.camera = None
        self.particle_emitter = None
        self.renderer = None
        self.ui = None
        
        self.init_game()
    
    def init_game(self):
        """Initialize game objects."""
        self.terrain = Terrain()
        # Spawn bike on first terrain segment
        spawn_height = self.terrain.get_height_at(100)
        self.bike = Bike(100, spawn_height)
        self.camera = Camera()
        self.particle_emitter = ParticleEmitter()
        self.ui = UI()
        self.score = 0
        self.multiplier = 1.0
        self.distance_traveled = 0
        self.last_position = self.bike.x
        self.game_time = 0
    
    def handle_input(self, events):
        """Process input events."""
        torque_input = 0
        
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "playing":
                        self.state = "menu"
                    elif self.state == "game_over":
                        self.state = "menu"
                
                if event.key == pygame.K_SPACE:
                    if self.state == "menu":
                        self.init_game()
                        self.state = "playing"
                    elif self.state == "game_over":
                        self.init_game()
                        self.state = "playing"
        
        # Continuous input for rotation
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
        if self.state == "playing":
            if keys[pygame.K_SPACE] or mouse_buttons[0]:
                torque_input = 1  # Clockwise rotation
        
        return True, torque_input
    
    def update(self):
        """Update game state."""
        if self.state != "playing":
            return
        
        self.game_time += 1
        
        # Get input
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        torque_input = 1 if (keys[pygame.K_SPACE] or mouse_buttons[0]) else 0
        
        # Update bike
        self.bike.update(self.terrain, torque_input)
        
        # Update terrain
        self.terrain.update(self.bike.x)
        
        # Update camera
        self.camera.update(self.bike.x, self.bike.y, self.bike.vx)
        
        # Update particles
        self.particle_emitter.update()
        
        # Update score based on distance
        distance_this_frame = self.bike.x - self.last_position
        self.distance_traveled += distance_this_frame
        self.score += distance_this_frame * SCORE_PER_DISTANCE * self.multiplier
        self.last_position = self.bike.x
        
        # Handle landing
        if self.bike.landed_this_frame:
            self.multiplier += MULTIPLIER_INCREMENT
            self.multiplier = min(self.multiplier, MULTIPLIER_MAX)
            self.score += SCORE_LANDING_BONUS * self.multiplier
            self.particle_emitter.emit_sparks(self.bike.x, self.bike.y, 15, COLOR_NEON_CYAN)
        
        # Handle flips
        flips = self.bike.get_flip_count()
        if flips > 0:
            self.score += flips * SCORE_PER_FLIP * self.multiplier
        
        # Check crash
        if self.bike.crash:
            self.multiplier = 1.0
            self.particle_emitter.emit_debris(self.bike.x, self.bike.y, 20, COLOR_NEON_MAGENTA)
            self.state = "game_over"
            if self.score > self.high_score:
                self.high_score = self.score
        
        # Difficulty scaling
        speed_multiplier = min(self.game_time * SPEED_INCREMENT_PER_SECOND / INITIAL_SPEED, MAX_DIFFICULTY_SPEED / INITIAL_SPEED)
        self.bike.vx = INITIAL_SPEED + (MAX_SPEED - INITIAL_SPEED) * min(self.game_time / (DIFFICULTY_RAMP_TIME * 60), 1.0)
    
    def render(self):
        """Render game frame."""
        self.surface.fill(COLOR_BG_DARK)
        
        if self.state == "menu":
            self.ui.draw_main_menu(self.surface)
        
        elif self.state == "playing":
            self.draw_background()
            self.draw_terrain()
            self.draw_particles()
            self.draw_bike()
            
            # Draw HUD
            flips = self.bike.get_flip_count()
            self.ui.draw_hud(self.surface, self.score, self.multiplier, self.bike.vx, flips)
        
        elif self.state == "game_over":
            self.ui.draw_game_over(self.surface, self.score, self.high_score)
        
        pygame.display.flip()
    
    def draw_background(self):
        """Draw gradient background with grid."""
        grid_size = 100
        start_x = int(self.camera.x // grid_size) * grid_size
        start_y = int(self.camera.y // grid_size) * grid_size
        
        for x in range(start_x, int(self.camera.x + WINDOW_WIDTH) + grid_size, grid_size):
            screen_x = x - self.camera.x
            pygame.draw.line(self.surface, COLOR_GRID, (screen_x, 0), (screen_x, WINDOW_HEIGHT), 1)
        
        for y in range(start_y, int(self.camera.y + WINDOW_HEIGHT) + grid_size, grid_size):
            screen_y = y - self.camera.y
            pygame.draw.line(self.surface, COLOR_GRID, (0, screen_y), (WINDOW_WIDTH, screen_y), 1)
    
    def draw_terrain(self):
        """Draw terrain segments."""
        segments = self.terrain.get_visible_segments(self.camera.x, WINDOW_WIDTH)
        
        for segment in segments:
            # Convert to screen coordinates
            start_screen = self.camera.world_to_screen(segment.start_x, segment.start_y)
            end_screen = self.camera.world_to_screen(segment.end_x, segment.end_y)
            
            # Draw segment line with glow effect
            pygame.draw.line(self.surface, COLOR_NEON_CYAN, start_screen, end_screen, 4)
            pygame.draw.line(self.surface, COLOR_NEON_YELLOW, start_screen, end_screen, 2)
    
    def draw_bike(self):
        """Draw bike with rotation."""
        import math
        screen_x, screen_y = self.camera.world_to_screen(self.bike.x, self.bike.y)
        screen_x = int(screen_x)
        screen_y = int(screen_y)
        
        # Only draw if on screen
        if -100 <= screen_x <= WINDOW_WIDTH + 100 and -100 <= screen_y <= WINDOW_HEIGHT + 100:
            # Draw bike body - much larger and more visible
            bike_width = 60
            bike_height = 30
            bike_surface = pygame.Surface((bike_width + 20, bike_height + 20), pygame.SRCALPHA)
            
            # Draw main body
            pygame.draw.rect(bike_surface, COLOR_NEON_MAGENTA, (10, 10, bike_width, bike_height), 0)
            pygame.draw.rect(bike_surface, COLOR_NEON_YELLOW, (10, 10, bike_width, bike_height), 3)
            
            # Rotate and blit
            rotated_bike = pygame.transform.rotate(bike_surface, -self.bike.angle)
            rotated_rect = rotated_bike.get_rect(center=(screen_x, screen_y))
            self.surface.blit(rotated_bike, rotated_rect)
            
            # Draw wheels
            rear_pos = self.bike.get_rear_wheel_pos()
            front_pos = self.bike.get_front_wheel_pos()
            
            rear_screen = self.camera.world_to_screen(rear_pos[0], rear_pos[1])
            front_screen = self.camera.world_to_screen(front_pos[0], front_pos[1])
            
            rear_screen = (int(rear_screen[0]), int(rear_screen[1]))
            front_screen = (int(front_screen[0]), int(front_screen[1]))
            
            # Draw larger wheels
            pygame.draw.circle(self.surface, COLOR_NEON_CYAN, rear_screen, 8)
            pygame.draw.circle(self.surface, COLOR_NEON_CYAN, front_screen, 8)
            pygame.draw.circle(self.surface, COLOR_NEON_YELLOW, rear_screen, 8, 2)
            pygame.draw.circle(self.surface, COLOR_NEON_YELLOW, front_screen, 8, 2)
    
    def draw_particles(self):
        """Draw particle effects."""
        for particle in self.particle_emitter.get_particles():
            screen_x, screen_y = self.camera.world_to_screen(particle.x, particle.y)
            
            # Clamp to screen
            if 0 <= screen_x < WINDOW_WIDTH and 0 <= screen_y < WINDOW_HEIGHT:
                color_with_alpha = particle.color
                pygame.draw.circle(self.surface, color_with_alpha, (int(screen_x), int(screen_y)), particle.size)
                
                # Draw glow
                glow_color = tuple(min(255, c + 50) for c in color_with_alpha)
                pygame.draw.circle(self.surface, glow_color, (int(screen_x), int(screen_y)), particle.size + 1, 1)
