# particles.py - Particle engine for visual effects

import random
import math
from settings import *

class Particle:
    """Individual particle with physics."""
    
    def __init__(self, x, y, vx, vy, lifetime, color, size=2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = size
    
    def update(self):
        """Update particle physics."""
        self.vy += GRAVITY * 0.5
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.vx *= 0.98
    
    def get_alpha(self):
        """Get alpha value for fade-out."""
        return int(255 * (self.lifetime / self.max_lifetime))
    
    def is_alive(self):
        """Check if particle is still alive."""
        return self.lifetime > 0

class ParticleEmitter:
    """Manages particle effects."""
    
    def __init__(self):
        self.particles = []
    
    def emit_sparks(self, x, y, count=10, color=COLOR_NEON_CYAN):
        """Emit spark particles."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2
            lifetime = random.randint(20, 40)
            particle = Particle(x, y, vx, vy, lifetime, color, size=3)
            self.particles.append(particle)
    
    def emit_debris(self, x, y, count=5, color=COLOR_NEON_MAGENTA):
        """Emit larger debris particles."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 1
            lifetime = random.randint(30, 60)
            particle = Particle(x, y, vx, vy, lifetime, color, size=5)
            self.particles.append(particle)
    
    def update(self):
        """Update all particles."""
        for particle in self.particles:
            particle.update()
        
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def get_particles(self):
        """Get all active particles."""
        return self.particles
