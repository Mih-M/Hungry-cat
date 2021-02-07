import pygame


class FishBone(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, screen_width):
        super().__init__()

        img = pygame.image.load('images/fish_bone.png').convert_alpha()
        self.image_right = pygame.transform.scale(img, (50, 50))
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.vel = 6
        self.max_x = screen_width

    def update(self):
        if self.direction == 1:
            self.image = self.image_right
        elif self.direction == -1:
            self.image = self.image_left

        self.rect.x += self.vel * self.direction

        if self.rect.right < 0 or self.rect.left > self.max_x:
            self.kill()
