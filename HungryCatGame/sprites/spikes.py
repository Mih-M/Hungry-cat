import pygame

from sprites.hitbox import Hitbox


class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, screen):
        super().__init__()

        self.screen = screen

        self.image = pygame.image.load('images/spike.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = self.screen.walking_area - self.rect.height

        self.hitbox = Hitbox(self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10)

    def update(self, move):
        self.rect.x -= move

        if self.rect.right < 0:
            self.kill()

        self.hitbox.update(self.rect.x + 5, self.rect.y + 5)
