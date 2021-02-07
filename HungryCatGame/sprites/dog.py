import pygame

from sprites.hitbox import Hitbox


class Dog(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.screen = screen

        self.walk_right = []
        self.walk_left = []

        for i in range(1, 9):
            img_right = pygame.image.load(f'images/dog/walk ({i}).png').convert_alpha()
            self.walk_right.append(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.walk_left.append(img_left)

        self.images = self.walk_left
        self.image_index = 0
        self.image_repeat = 5
        self.image = self.images[self.image_index]

        self.rect = self.image.get_rect()
        self.rect.x = self.screen.width - self.rect.width
        self.rect.y = self.screen.walking_area - self.rect.height

        self.vel_x = 20
        self.direction = -1

        self.lives = 5

        self.hitbox = Hitbox(self.rect.x + 10, self.rect.y + 10, 90, 70)

        self.appear = False

        self.attack = False
        self.count_attack_moves = 0
        self.dead = False

    def hit(self):
        self.lives -= 1
        if self.lives == 0:
            self.dead = True

    def change_direction(self):
        if self.direction == -1:
            self.direction = 1
            self.images = self.walk_right
        else:
            self.direction = -1
            self.images = self.walk_left

        self.count_attack_moves += 1

    def update(self):
        if self.dead:
            self.rect.y += 2
        elif self.attack:
            self.rect.x += self.vel_x * self.direction
            if self.count_attack_moves == 2:
                self.attack = False
                self.count_attack_moves = 0

        self.image_index += 1
        if self.image_index + 1 >= len(self.images) * self.image_repeat:
            self.image_index = 0

        self.image = self.images[self.image_index // self.image_repeat]

        if self.rect.x < 0 or self.rect.x + self.rect.width > self.screen.width:
            self.change_direction()

        if self.rect.y > self.screen.height:
            self.kill()

        self.hitbox.update(self.rect.x + 10, self.rect.y + 10)

