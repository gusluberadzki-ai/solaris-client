# ui.py - User interface and HUD

import pygame
from settings import *

class UI:
    """Manages all UI rendering and state."""
    
    def __init__(self):
        try:
            # Try to load a nice font, fall back to default
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
        except:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
    
    def draw_hud(self, surface, score, multiplier, speed, flips):
        """Draw in-game HUD."""
        # Score
        score_text = self.font_medium.render(f"Score: {int(score)}", True, COLOR_NEON_CYAN)
        surface.blit(score_text, (20, 20))
        
        # Multiplier
        mult_color = COLOR_NEON_MAGENTA if multiplier > 1.0 else COLOR_NEON_CYAN
        mult_text = self.font_medium.render(f"Multiplier: {multiplier:.1f}x", True, mult_color)
        surface.blit(mult_text, (20, 70))
        
        # Speed
        speed_text = self.font_small.render(f"Speed: {speed:.1f}", True, COLOR_NEON_YELLOW)
        surface.blit(speed_text, (20, 120))
        
        # Flips
        flips_text = self.font_small.render(f"Flips: {flips}", True, COLOR_NEON_PURPLE)
        surface.blit(flips_text, (20, 150))
    
    def draw_main_menu(self, surface):
        """Draw main menu."""
        surface.fill(COLOR_BG_DARK)
        
        # Title
        title = self.font_large.render("NEON RIDER", True, COLOR_NEON_CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        surface.blit(title, title_rect)
        
        # Instructions
        instr1 = self.font_small.render("Hold SPACE or MOUSE to rotate", True, COLOR_NEON_YELLOW)
        instr_rect = instr1.get_rect(center=(WINDOW_WIDTH // 2, 250))
        surface.blit(instr1, instr_rect)
        
        instr2 = self.font_small.render("Land safely to survive", True, COLOR_NEON_YELLOW)
        instr_rect2 = instr2.get_rect(center=(WINDOW_WIDTH // 2, 290))
        surface.blit(instr2, instr_rect2)
        
        # Play button
        play_text = self.font_medium.render("PRESS SPACE TO START", True, COLOR_NEON_MAGENTA)
        play_rect = play_text.get_rect(center=(WINDOW_WIDTH // 2, 400))
        surface.blit(play_text, play_rect)
        
        # Quit button
        quit_text = self.font_small.render("Press ESC to quit", True, COLOR_NEON_PURPLE)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, 550))
        surface.blit(quit_text, quit_rect)
    
    def draw_game_over(self, surface, score, high_score):
        """Draw game over screen."""
        surface.fill(COLOR_BG_DARK)
        
        # Game Over
        game_over = self.font_large.render("GAME OVER", True, COLOR_NEON_MAGENTA)
        game_over_rect = game_over.get_rect(center=(WINDOW_WIDTH // 2, 100))
        surface.blit(game_over, game_over_rect)
        
        # Score
        score_text = self.font_medium.render(f"Score: {int(score)}", True, COLOR_NEON_CYAN)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        surface.blit(score_text, score_rect)
        
        # High Score
        high_score_text = self.font_medium.render(f"High Score: {int(high_score)}", True, COLOR_NEON_YELLOW)
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, 320))
        surface.blit(high_score_text, high_score_rect)
        
        # Restart
        restart_text = self.font_small.render("Press SPACE to restart", True, COLOR_NEON_MAGENTA)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, 450))
        surface.blit(restart_text, restart_rect)
        
        # Quit
        quit_text = self.font_small.render("Press ESC for menu", True, COLOR_NEON_PURPLE)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, 500))
        surface.blit(quit_text, quit_rect)
