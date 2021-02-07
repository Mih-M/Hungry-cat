import pygame


class Water(pygame.sprite.Sprite):
    def __init__(self, x, screen):
        super().__init__()

        self.screen = screen

        self.image = pygame.image.load('images/water.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = self.screen.walking_area - 4

    def update(self, move):
        self.rect.x -= move

        if self.rect.right < 0:
            self.kill()

