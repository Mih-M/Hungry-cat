import pygame


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)

    def update(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y
