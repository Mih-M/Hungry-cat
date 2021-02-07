import pygame

from sprites.fish_bone import FishBone
from sprites.hitbox import Hitbox


class Cat(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.screen = screen

        self.idle_right = []
        self.idle_left = []

        self.run_right = []
        self.run_left = []

        self.jump_right = []
        self.jump_left = []

        self.hurt_right = []
        self.hurt_left = []

        self.dead_right = []
        self.dead_left = []

        for i in range(1, 11):
            img = pygame.image.load(f'images/cat/Idle ({i}).png').convert_alpha()
            img_right = pygame.transform.scale(img, (115, 100))
            self.idle_right.append(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.idle_left.append(img_left)

        for i in range(1, 9):
            img = pygame.image.load(f'images/cat/Run ({i}).png').convert_alpha()
            img_right = pygame.transform.scale(img, (115, 100))
            self.run_right.append(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.run_left.append(img_left)

        for i in range(1, 9):
            img = pygame.image.load(f'images/cat/Jump ({i}).png').convert_alpha()
            img_right = pygame.transform.scale(img, (115, 100))
            self.jump_right.append(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.jump_left.append(img_left)

        for i in range(1, 11):
            img = pygame.image.load(f'images/cat/Hurt ({i}).png').convert_alpha()
            img_right = pygame.transform.scale(img, (115, 100))
            self.hurt_right.append(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.hurt_left.append(img_left)

        for i in range(1, 11):
            img = pygame.image.load(f'images/cat/Dead ({i}).png').convert_alpha()
            img_right = pygame.transform.scale(img, (115, 100))
            self.dead_right.append(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.dead_left.append(img_left)

        self.images = self.idle_right
        self.image_index = 0
        self.image_repeat = 5
        self.image = self.images[self.image_index]

        self.rect = self.image.get_rect()

        self.max_x = self.screen.width - self.rect.width
        self.max_y = self.screen.walking_area - self.rect.height

        self.rect.x = 20
        self.rect.y = self.max_y

        self.hitbox = Hitbox(self.rect.x + 20, self.rect.y, 60, 100)

        self.vel_x = 5
        self.vel_y = 0

        self.fish_bones_thrown = pygame.sprite.Group()
        self.fish_bones_collected = 0
        self.last_shoot = 0

        self.jumped = False
        self.last_jump = 0

        self.right = False
        self.left = False
        self.direction = 1

        self.hurt = False
        self.hurt_duration = 150
        self.hurt_time = self.hurt_duration

        self.lives = 3

        self.dead = False

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > 200:
            self.last_shoot = now
            return True
        return False

    def can_jump(self):
        now = pygame.time.get_ticks()
        if now - self.last_jump > 700:
            self.last_jump = now
            return True
        return False

    def update(self, keys):
        dx = 0
        dy = 0

        self.image_index += 1

        if self.lives == 0 and not self.dead:
            self.dead = True
            self.image_index = 0
            self.rect.y = self.max_y

        if self.dead:
            if self.image_index + 1 > len(self.dead_left) * self.image_repeat:
                return

            if self.direction == 1:
                self.images = self.dead_right
            elif self.direction == -1:
                self.images = self.dead_left

        else:
            if self.hurt:
                self.hurt_time -= 1
                if self.hurt_time == 0:
                    self.hurt = False
                    self.hurt_time = self.hurt_duration
                    self.image_index = 0

                if self.direction == 1:
                    self.images = self.hurt_right
                elif self.direction == -1:
                    self.images = self.hurt_left

            elif self.jumped:
                if self.direction == 1:
                    self.images = self.jump_right
                elif self.direction == -1:
                    self.images = self.jump_left

            elif not self.left and not self.right and not self.jumped:
                if self.direction == 1:
                    self.images = self.idle_right
                elif self.direction == -1:
                    self.images = self.idle_left

            if self.image_index + 1 >= len(self.images) * self.image_repeat:
                self.image_index = 0

            if keys[pygame.K_LEFT]:
                if self.rect.x - self.vel_x >= -20:
                    dx -= self.vel_x
                    if not self.jumped:
                        if not self.left:
                            self.image_index = 0
                        if not self.hurt:
                            self.images = self.run_left
                    self.right = False
                    self.left = True
                    self.direction = -1
            elif keys[pygame.K_RIGHT]:
                if self.rect.x + self.vel_x <= self.max_x:
                    dx += self.vel_x
                    if not self.jumped:
                        if not self.right:
                            self.image_index = 0
                        if not self.hurt:
                            self.images = self.run_right
                    self.right = True
                    self.left = False
                    self.direction = 1
            else:
                self.right = False
                self.left = False

            if keys[pygame.K_UP] and not self.jumped and self.can_jump():
                self.vel_y = -20
                self.jumped = True
                self.image_index = 0

            if keys[pygame.K_SPACE] and self.can_shoot():
                if self.fish_bones_collected > 0 and len(self.fish_bones_thrown) < 2:
                    fish_bone = FishBone(self.rect.center[0], self.rect.center[1], self.direction, self.screen.width)
                    self.fish_bones_thrown.add(fish_bone)
                    self.fish_bones_collected -= 1

            if (self.rect.y + self.vel_y <= self.max_y) and self.jumped:
                dy += self.vel_y
                self.vel_y += 1
            elif self.jumped:
                dy = self.max_y - self.rect.y
                self.vel_y = 0
                self.jumped = False

            self.rect.move_ip(dx, dy)

        self.image = self.images[self.image_index // self.image_repeat]
        self.hitbox.update(self.rect.x + 20, self.rect.y)

    def draw(self):
        self.screen.window.blit(self.image, self.rect)
        # pygame.draw.rect(self.screen.window, (255, 0, 0), self.rect, 2)
        # pygame.draw.rect(self.screen.window, (0, 0, 0), self.hitbox.rect, 2)
        for fb in self.fish_bones_thrown:
            fb.update()
            self.screen.window.blit(fb.image, fb.rect)
