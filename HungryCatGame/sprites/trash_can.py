import pygame


class TrashCan(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.screen = screen

        self.image = pygame.image.load('images/trash_can.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = screen.width - self.rect.width
        self.rect.y = self.screen.walking_area - self.rect.height + 10
