import pygame


class Rat(pygame.sprite.Sprite):
    def __init__(self, x, screen):
        super().__init__()

        self.screen = screen

        self.run_images = []
        self.hit_images = []

        for i in range(1, 6):
            img = pygame.image.load(f'images/rat/walk ({i}).tif').convert_alpha()
            img = pygame.transform.scale(img, (75, 50))
            img = pygame.transform.flip(img, True, False)
            self.run_images.append(img)

        for i in range(1, 3):
            img = pygame.image.load(f'images/rat/hit ({i}).tif').convert_alpha()
            img = pygame.transform.scale(img, (75, 50))
            img = pygame.transform.flip(img, True, False)
            self.hit_images.append(img)

        self.images = self.run_images
        self.image_index = 0
        self.image_repeat = 5
        self.image = self.images[self.image_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = self.screen.walking_area - self.rect.height
        self.vel_x = 2

        self.dead = False

    def hit(self):
        self.dead = True
        self.images = self.hit_images

    def update(self, move):
        if self.dead:
            self.rect.y += 2
            self.rect.x -= move
        else:
            self.rect.x -= self.vel_x + move

        self.image_index += 1
        if self.image_index + 1 >= len(self.images) * self.image_repeat:
            self.image_index = 0

        self.image = self.images[self.image_index // self.image_repeat]

        if self.rect.right < 0 or self.rect.y > self.screen.height:
            self.kill()
