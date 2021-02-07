import pygame


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('images/grass_piece.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, move):
        self.rect.x -= move

        if self.rect.right < 0:
            self.kill()
