import pygame


class Background:
    def __init__(self, screen):
        self.screen = screen

        img = pygame.image.load('images/bg.png').convert()
        img = pygame.transform.scale(img, (900, 550))

        self.first_image = img
        self.second_image = pygame.transform.flip(img, True, False)

        self.x = -1
        self.rel_x = 0

    def update(self, move):
        self.x -= move

        if self.x <= -self.screen.width:
            self.x = -1
            self.first_image, self.second_image = self.second_image, self.first_image

    def draw(self):
        self.screen.window.blit(self.first_image, (self.x, 0))
        self.screen.window.blit(self.second_image, (self.screen.width + self.x, 0))
