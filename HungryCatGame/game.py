from collections import deque

import pygame

from sprites.cat import Cat
from sprites.dog import Dog
from sprites.fish import Fish
from game_info import GameInfo
from sprites.grass import Grass
from sprites.rat import Rat
from sprites.spikes import Spikes
from sprites.trash_can import TrashCan
from sprites.water import Water


class Game:
    def __init__(self, screen, background, add_dog_attack):
        self.screen = screen
        self.bg = background
        self.add_dog_attack = add_dog_attack

        self.cat = Cat(screen)
        self.dog = Dog(screen)

        self.game_info = GameInfo(screen, self.cat, self.dog)

        self.fish_queue = deque(Game.read_coordinates('files/fish_queue.txt', True))
        self.next_fish = self.fish_queue.popleft()

        self.grass_queue = deque(Game.read_coordinates('files/grass_queue.txt', True))
        self.next_grass = self.grass_queue.popleft()

        self.spikes_queue = deque(Game.read_coordinates('files/spikes_queue.txt'))
        self.next_spikes = self.spikes_queue.popleft()

        self.water_queue = deque(Game.read_coordinates('files/water_queue.txt'))
        self.next_water = self.water_queue.popleft()

        self.rat_queue = deque(Game.read_coordinates('files/rat_queue.txt'))
        self.next_rat = self.rat_queue.popleft()

        self.fish_group = pygame.sprite.Group(Fish(200, 200), Fish(500, 300), Fish(600, 100))
        self.grass_group = pygame.sprite.Group(Grass(300, 300), Grass(600, 200))
        self.spikes_group = pygame.sprite.Group(Spikes(950, self.screen))
        self.water_group = pygame.sprite.Group(Water(1200, self.screen))
        self.rat_group = pygame.sprite.Group(Rat(700, self.screen))
        self.dog_group = pygame.sprite.Group()
        self.trash_group = pygame.sprite.Group()

        self.count_moves = 0

    @staticmethod
    def read_coordinates(file, multiple_values: bool = False):
        coordinates_list = []

        with open(file, 'r') as file:
            for coordinates in file.read().split(';'):
                if multiple_values:
                    coordinates_list.append(tuple(map(int, coordinates.split('-'))))
                else:
                    coordinates_list.append(int(coordinates))

        return coordinates_list

    def game_loop(self, pressed_keys):
        move = 0

        if not self.dog.appear and self.cat.rect.x > self.screen.width // 2 - self.cat.rect.width // 2:
            self.cat.rect.x = self.screen.width // 2 - self.cat.rect.width // 2
            move = 4
            self.count_moves += 1

        self.bg.update(move)

        if self.count_moves == 1750:
            self.dog.appear = True
            self.dog_group.add(self.dog)
            self.trash_group.add(TrashCan(self.screen))
            pygame.time.set_timer(self.add_dog_attack, 1000)
            self.count_moves = 0

        if self.count_moves == self.next_fish[0]:
            self.fish_group.add(Fish(self.screen.width, self.next_fish[1]))
            if self.fish_queue:
                self.next_fish = self.fish_queue.popleft()

        if self.count_moves == self.next_grass[0]:
            self.grass_group.add(Grass(self.screen.width, self.next_grass[1]))
            if self.grass_queue:
                self.next_grass = self.grass_queue.popleft()

        if self.count_moves == self.next_spikes:
            self.spikes_group.add(Spikes(self.screen.width, self.screen))
            if self.spikes_queue:
                self.next_spikes = self.spikes_queue.popleft()

        if self.count_moves == self.next_water:
            self.water_group.add(Water(self.screen.width, self.screen))
            if self.water_queue:
                self.next_water = self.water_queue.popleft()

        if self.count_moves == self.next_rat:
            self.rat_group.add(Rat(self.screen.width, self.screen))
            if self.rat_queue:
                self.next_rat = self.rat_queue.popleft()

        self.trash_group.draw(self.screen.window)

        self.water_group.update(move)
        self.water_group.draw(self.screen.window)

        self.cat.update(pressed_keys)
        self.cat.draw()

        self.fish_group.update(move)
        self.fish_group.draw(self.screen.window)

        self.grass_group.update(move)
        self.grass_group.draw(self.screen.window)

        self.spikes_group.update(move)
        self.spikes_group.draw(self.screen.window)

        self.rat_group.update(move)
        self.rat_group.draw(self.screen.window)

        self.dog_group.update()
        self.dog_group.draw(self.screen.window)

        if pygame.sprite.spritecollide(self.cat.hitbox, self.fish_group, True):
            self.cat.fish_bones_collected += 1

        if grass_list := pygame.sprite.spritecollide(self.cat.hitbox, self.grass_group, False):
            grass = grass_list[0].rect
            hitbox = self.cat.hitbox.rect

            cat_y_on_top = grass.top - self.cat.rect.height + 1

            if hitbox.bottom <= grass.top + self.cat.vel_y and \
                    (hitbox.left + 10 < grass.right and
                     hitbox.right - 10 > grass.left):
                self.cat.jumped = False
                self.cat.rect.y = cat_y_on_top

            elif grass.top < hitbox.top <= grass.bottom:
                if self.cat.vel_y < 0:
                    self.cat.vel_y = 1

            elif (hitbox.y == cat_y_on_top) and (hitbox.left + 10 >= grass.right or hitbox.right - 10 <= grass.left):
                self.cat.vel_y = 1
                self.cat.jumped = True

            elif hitbox.x < grass.left <= hitbox.right:
                self.cat.rect.x = grass.left - self.cat.rect.width + 20

            elif hitbox.x > grass.left and hitbox.left <= grass.right:
                self.cat.rect.x = grass.right - 20

        if bone_rat_dict := pygame.sprite.groupcollide(self.cat.fish_bones_thrown, self.rat_group, False, False):
            for bone, rats in bone_rat_dict.items():
                rat = rats[0]
                if not rat.dead:
                    rat.hit()
                    self.game_info.score += 10
                    bone.kill()

        if bone_dog_dict := pygame.sprite.groupcollide(self.cat.fish_bones_thrown, self.dog_group, False, False):
            for bone, dog_list in bone_dog_dict.items():
                dog = dog_list[0]
                if not dog.dead:
                    dog.hit()
                    self.game_info.score += 20
                    bone.kill()

        if water_rat_dict := pygame.sprite.groupcollide(self.water_group, self.rat_group, False, False):
            for water, rats in water_rat_dict.items():
                for rat in rats:
                    if rat.rect.right <= water.rect.right:
                        rat.hit()

        if rat_list := pygame.sprite.spritecollide(self.cat.hitbox, self.rat_group, False):
            for rat in rat_list:
                if not self.cat.hurt and not rat.dead:
                    self.cat.hurt = True
                    self.cat.lives -= 1

        if pygame.sprite.collide_rect(self.cat.hitbox, self.dog.hitbox):
            if not self.cat.hurt:
                self.cat.hurt = True
                self.cat.lives -= 1

        for spike in self.spikes_group:
            if pygame.sprite.collide_rect(self.cat.hitbox, spike.hitbox):
                if not self.cat.hurt:
                    self.cat.hurt = True
                    self.cat.lives -= 1

        if water_list := pygame.sprite.spritecollide(self.cat.hitbox, self.water_group, False):
            water = water_list[0].rect
            hitbox = self.cat.hitbox.rect

            if hitbox.left + 10 >= water.left and hitbox.right - 10 <= water.right and not self.cat.jumped:
                self.cat.rect.y = self.cat.max_y + 20
                if not self.cat.hurt:
                    self.cat.hurt = True
                    self.cat.lives -= 1

            if self.cat.rect.y > self.cat.max_y:
                if hitbox.left < water.left:
                    self.cat.rect.x = water.left - 20
                elif hitbox.right > water.right:
                    self.cat.rect.x = water.right - 20 - self.cat.hitbox.rect.width

        self.game_info.update()
