# physics.py - Simplified rigid-body physics engine

import math
from settings import *

class Bike:
    """Represents a motorcycle with physics properties."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = INITIAL_SPEED  # Forward velocity
        self.vy = 0  # Vertical velocity (affected by gravity)
        self.angle = 0  # Rotation in degrees (0 = upright)
        self.angular_velocity = 0  # Rotation speed
        self.is_airborne = False
        self.landed_this_frame = False
        self.crash = False
        
        # Wheel positions relative to bike center
        self.rear_wheel_offset = -15
        self.front_wheel_offset = 15
    
    def get_rear_wheel_pos(self):
        """Get world position of rear wheel."""
        rad = math.radians(self.angle)
        offset_x = self.rear_wheel_offset * math.cos(rad)
        offset_y = self.rear_wheel_offset * math.sin(rad)
        return (self.x + offset_x, self.y + offset_y)
    
    def get_front_wheel_pos(self):
        """Get world position of front wheel."""
        rad = math.radians(self.angle)
        offset_x = self.front_wheel_offset * math.cos(rad)
        offset_y = self.front_wheel_offset * math.sin(rad)
        return (self.x + offset_x, self.y + offset_y)
    
    def apply_torque(self, torque_direction):
        """Apply rotational force. torque_direction: 1 (clockwise), -1 (counter), 0 (none)."""
        if torque_direction != 0:
            self.angular_velocity += torque_direction * ANGULAR_TORQUE
        else:
            # Dampen rotation when no input
            self.angular_velocity *= 0.95
    
    def update(self, terrain, apply_torque_input):
        """Update bike physics."""
        self.landed_this_frame = False
        
        if self.crash:
            # Dead bike slides to a stop
            self.vx *= FRICTION
            if self.vx < 0.1:
                self.vx = 0
            self.x += self.vx
            self.vy += GRAVITY
            self.y += self.vy
            return
        
        # Apply acceleration
        self.vx += ACCELERATION
        self.vx = min(self.vx, MAX_SPEED)
        
        # Apply gravity
        self.vy += GRAVITY
        self.vy *= AIR_RESISTANCE
        
        # Apply air resistance to forward velocity
        self.vx *= 0.99
        
        # Move bike
        self.x += self.vx
        self.y += self.vy
        
        # Apply torque input
        self.apply_torque(apply_torque_input)
        
        # Update rotation
        self.angle += self.angular_velocity
        self.angular_velocity *= 0.97  # Damping
        
        # Collision detection with terrain
        self.check_terrain_collision(terrain)
    
    def check_terrain_collision(self, terrain):
        """Check collision with terrain and resolve."""
        rear_wheel = self.get_rear_wheel_pos()
        front_wheel = self.get_front_wheel_pos()
        
        # Get terrain height at wheel positions
        rear_height = terrain.get_height_at(rear_wheel[0])
        front_height = terrain.get_height_at(front_wheel[0])
        
        # Average terrain height under bike
        avg_terrain_height = (rear_height + front_height) / 2
        
        # Check if wheels are below terrain (collision)
        rear_below = rear_wheel[1] > rear_height
        front_below = front_wheel[1] > front_height
        
        if rear_below or front_below:
            # Collision detected
            # Determine landing angle safety
            bike_angle = self.angle % 360
            if bike_angle > 180:
                bike_angle -= 360
            
            # Check if landing is safe (only when airborne)
            if self.is_airborne:
                # Landing from air - check angle and rotation
                if abs(bike_angle) > LANDING_ANGLE_TOLERANCE or abs(self.angular_velocity) > CRASH_ANGULAR_VELOCITY_THRESHOLD:
                    self.crash = True
                    return
                
                # Safe landing
                self.is_airborne = False
                self.landed_this_frame = True
                self.vy = 0
                self.angle = 0
                self.angular_velocity = 0
            else:
                # Already on ground - crash if angle is bad
                if abs(bike_angle) > LANDING_ANGLE_TOLERANCE or abs(self.angular_velocity) > CRASH_ANGULAR_VELOCITY_THRESHOLD:
                    self.crash = True
                    return
            
            # Always place on ground when colliding
            self.y = avg_terrain_height
        else:
            # No collision - in air
            self.is_airborne = True
    
    def get_flip_count(self):
        """Calculate number of flips completed."""
        return int(abs(self.angle) / 360)
    
    def reset_position(self, x, y):
        """Reset bike to starting position."""
        self.x = x
        self.y = y
        self.vx = INITIAL_SPEED
        self.vy = 0
        self.angle = 0
        self.angular_velocity = 0
        self.is_airborne = False
        self.crash = False
