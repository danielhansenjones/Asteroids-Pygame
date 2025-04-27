import pygame
from circleshape import *
import random
from constants import *



class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), self.position, self.radius, width = 2)


    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        new_astroid_1_vel = self.velocity.rotate(random_angle) * 1.2
        new_astroid_2_vel = self.velocity.rotate(-random_angle) * 1.2
        new_astroid_radius = self.radius - ASTEROID_MIN_RADIUS
        new_astroid_1 = Asteroid(self.position.x, self.position.y, new_astroid_radius)
        new_astroid_1.velocity = new_astroid_1_vel
        new_astroid_2 = Asteroid(self.position.x, self.position.y, new_astroid_radius)
        new_astroid_2.velocity = new_astroid_2_vel