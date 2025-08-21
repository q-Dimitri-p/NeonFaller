import pygame

class Player:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.movement = 0
        self.gravity = 0.5
        self.jump_strength = -8

    def update(self):
        self.movement += self.gravity
        self.rect.centery += self.movement

    def jump(self):
        self.movement = self.jump_strength

    def draw(self, screen):
        screen.blit(self.image, self.rect)
