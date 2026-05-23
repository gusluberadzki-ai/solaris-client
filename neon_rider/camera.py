# camera.py - Smooth camera system

import math
from settings import *

class Camera:
    """Manages smooth camera following and viewport."""
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
    
    def update(self, player_x, player_y, player_vx):
        """Update camera to follow player smoothly."""
        # Calculate target position with lookahead
        self.target_x = player_x + CAMERA_LOOKAHEAD
        self.target_y = player_y - WINDOW_HEIGHT // 3
        
        # Smooth follow
        self.x += (self.target_x - self.x) * CAMERA_FOLLOW_SPEED
        self.y += (self.target_y - self.y) * CAMERA_FOLLOW_SPEED
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates."""
        screen_x = world_x - self.x
        screen_y = world_y - self.y
        return (screen_x, screen_y)
    
    def get_viewport(self):
        """Get current camera viewport bounds in world coordinates."""
        return (self.x, self.y, self.x + WINDOW_WIDTH, self.y + WINDOW_HEIGHT)
