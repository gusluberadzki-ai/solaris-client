# terrain.py - Procedural terrain generation

import random
import math
from settings import *

class TerrainSegment:
    """Represents a section of terrain."""
    
    def __init__(self, start_x, start_y, end_x, end_y, segment_type="flat"):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.segment_type = segment_type  # "flat", "ramp_up", "ramp_down", "loop", "gap"
    
    def get_height_at(self, x):
        """Get terrain height at world x coordinate (linear interpolation)."""
        if x < self.start_x or x > self.end_x:
            return None
        
        t = (x - self.start_x) / (self.end_x - self.start_x)
        return self.start_y + (self.end_y - self.start_y) * t

class Terrain:
    """Manages procedural terrain generation."""
    
    def __init__(self):
        self.segments = []
        self.next_x = 0
        self.current_height = WINDOW_HEIGHT - 200
        self.segment_index = 0
        self.generate_initial_terrain()
    
    def generate_initial_terrain(self):
        """Create initial terrain."""
        self.current_height = WINDOW_HEIGHT - 200
        self.next_x = 0
        for _ in range(50):
            self.add_random_segment()
    
    def add_random_segment(self):
        """Add a new random terrain segment."""
        segment_length = random.randint(80, 150)
        segment_types = ["flat", "ramp_up", "ramp_down", "ramp_up", "ramp_down"]
        segment_type = random.choice(segment_types)
        
        start_x = self.next_x
        start_y = self.current_height
        end_x = start_x + segment_length
        
        if segment_type == "flat":
            end_y = start_y
        elif segment_type == "ramp_up":
            end_y = start_y - random.randint(20, 60)
        elif segment_type == "ramp_down":
            end_y = start_y + random.randint(20, 60)
        
        # Clamp height
        end_y = max(MIN_TERRAIN_HEIGHT, min(MAX_TERRAIN_HEIGHT, end_y))
        
        segment = TerrainSegment(start_x, start_y, end_x, end_y, segment_type)
        self.segments.append(segment)
        
        self.next_x = end_x
        self.current_height = end_y
    
    def update(self, player_x):
        """Generate new terrain ahead of player, despawn behind."""
        # Despawn old segments
        self.segments = [s for s in self.segments if s.end_x > player_x - TERRAIN_DESPAWN_DISTANCE]
        
        # Generate new segments
        while self.next_x < player_x + TERRAIN_SPAWN_DISTANCE:
            self.add_random_segment()
    
    def get_height_at(self, x):
        """Get terrain height at world x coordinate."""
        for segment in self.segments:
            if segment.start_x <= x <= segment.end_x:
                return segment.get_height_at(x)
        
        # Return default if out of range
        return WINDOW_HEIGHT - 100
    
    def get_visible_segments(self, camera_x, camera_width):
        """Get segments visible on screen."""
        return [s for s in self.segments if s.end_x > camera_x and s.start_x < camera_x + camera_width]
