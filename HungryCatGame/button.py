import pygame

from sprites.hitbox import Hitbox


class Button:
    def __init__(self, screen, text, y):
        self.screen = screen
        self.text = text
        self.font = pygame.font.Font('Caveat.ttf', 35)

        self.display_text = self.font.render(f'{self.text}', True, (0, 0, 0))
        self.rect = self.display_text.get_rect()
        self.rect.x = screen.width / 2 - self.rect.width / 2
        self.rect.y = y

        self.hitbox = Hitbox(self.rect.x - 10, self.rect.y - 6, self.rect.width + 20, self.rect.height + 10)

    def draw(self):
        self.screen.window.blit(self.display_text, self.rect)

    def draw_border(self):
        pygame.draw.rect(self.screen.window, (0, 0, 0), self.hitbox.rect, 2)
