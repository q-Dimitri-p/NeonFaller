import pygame
import random

class Obstacle:
    def __init__(self, image_path, x, height):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.x = x
        self.width = self.image.get_width()
        self.height = height
        self.gap = 180
        self.speed = 4

        # Randomize gap position
        self.top_height = random.randint(0, self.height - self.gap - 100)
        self.bottom_height = self.height - self.top_height - self.gap

        self.rect_top = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.rect_bottom = pygame.Rect(self.x, self.top_height + self.gap, self.width, self.bottom_height)
        self.scored = False

    def update(self):
        self.rect_top.x -= self.speed
        self.rect_bottom.x -= self.speed

    def draw(self, surface):
        # Draw top obstacle (flipped and scaled)
        top_img = pygame.transform.scale(self.image, (self.width, self.top_height))
        top_img = pygame.transform.flip(top_img, False, True)
        surface.blit(top_img, (self.rect_top.x, self.rect_top.y))

        # Draw bottom obstacle (scaled)
        bottom_img = pygame.transform.scale(self.image, (self.width, self.bottom_height))
        surface.blit(bottom_img, (self.rect_bottom.x, self.rect_bottom.y))

    def off_screen(self):
        return self.rect_top.right < 0
