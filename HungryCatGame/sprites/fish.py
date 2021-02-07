import pygame


class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.images = []

        for i in range(1, 3):
            img = pygame.image.load(f'images/fish/fish ({i}).png').convert_alpha()
            self.images.append(img)

        self.image_index = 0
        self.image_repeat = 30
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, move):
        self.image_index += 1
        if self.image_index + 1 >= len(self.images) * self.image_repeat:
            self.image_index = 0

        self.image = self.images[self.image_index // self.image_repeat]

        self.rect.x -= move

        if self.rect.x < 0 - self.rect.width:
            self.kill()
