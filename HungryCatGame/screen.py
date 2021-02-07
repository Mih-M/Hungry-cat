import pygame


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        self.walking_area = self.height - 57
