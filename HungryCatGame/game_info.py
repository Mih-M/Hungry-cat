from collections import deque

import pygame


class GameInfo:
    def __init__(self, screen, cat, dog):
        self.screen = screen
        self.cat = cat
        self.dog = dog
        self.score = 0

        cat_img = pygame.image.load('images/cat_head.png').convert_alpha()
        fish_img = pygame.image.load('images/fish_bone.png').convert_alpha()
        self.dog_img = pygame.image.load('images/dog_head.png').convert_alpha()

        self.cat_img = pygame.transform.scale(cat_img, (40, 40))
        self.cat_rect = self.cat_img.get_rect()
        self.cat_rect.x = 10
        self.cat_rect.y = 10

        self.fish_img = pygame.transform.scale(fish_img, (40, 40))
        self.fish_rect = self.fish_img.get_rect()
        self.fish_rect.x = 10
        self.fish_rect.y = 60

        self.dog_rect = self.dog_img.get_rect()
        self.dog_rect.x = screen.width - 120
        self.dog_rect.y = 60

        self.font_small = pygame.font.Font('Caveat.ttf', 30)
        self.font_large = pygame.font.Font('Caveat.ttf', 60)

        self.cat_lives_text = self.font_small.render(f'{self.cat.lives}', True, (0, 0, 0))
        self.cat_lives_text_rect = self.cat_lives_text.get_rect()
        self.cat_lives_text_rect.x = 60
        self.cat_lives_text_rect.y = self.cat_rect.center[1] - self.cat_lives_text_rect.height / 2

        self.fish_text = self.font_small.render(f'{self.cat.fish_bones_collected}', True, (0, 0, 0))
        self.fish_text_rect = self.fish_text.get_rect()
        self.fish_text_rect.x = 60
        self.fish_text_rect.y = self.fish_rect.center[1] - self.fish_text_rect.height / 2

        self.dog_lives_text = self.font_small.render(f'{self.dog.lives}', True, (0, 0, 0))
        self.dog_lives_text_rect = self.dog_lives_text.get_rect()
        self.dog_lives_text_rect.x = self.dog_rect.right + 10
        self.dog_lives_text_rect.y = self.dog_rect.center[1] - self.dog_lives_text_rect.height / 2

        self.score_text = self.font_small.render(f'Score: {self.score}', True, (0, 0, 0))
        self.score_text_rect = self.score_text.get_rect()
        self.score_text_rect.x = screen.width - 130
        self.score_text_rect.y = 10

        self.win_text = self.font_large.render('Y O U   W O N !', True, (0, 0, 0))
        self.win_text_rect = self.win_text.get_rect()
        self.win_text_rect.x = screen.width / 2 - self.win_text_rect.width / 2
        self.win_text_rect.y = 50
        self.win_letters_queue = deque(list('Y O U   W O N !'))
        self.win_text_current = ''

        self.game_over_text = self.font_large.render('G A M E   O V E R !', True, (0, 0, 0))
        self.game_over_text_rect = self.game_over_text.get_rect()
        self.game_over_text_rect.x = screen.width / 2 - self.game_over_text_rect.width / 2
        self.game_over_text_rect.y = 50
        self.game_over_letters_queue = deque(list('G A M E   O V E R !'))
        self.game_over_text_current = ''

        self.delay_letter = 0

    def update(self):
        self.cat_lives_text = self.font_small.render(f'{self.cat.lives}', True, (0, 0, 0))
        self.fish_text = self.font_small.render(f'{self.cat.fish_bones_collected}', True, (0, 0, 0))
        self.dog_lives_text = self.font_small.render(f'{self.dog.lives}', True, (0, 0, 0))
        self.score_text = self.font_small.render(f'Score: {self.score}', True, (0, 0, 0))

        if self.dog.dead:
            self.delay_letter += 1

            if len(self.win_letters_queue) > 0 and self.delay_letter == 5:
                self.win_text_current += self.win_letters_queue.popleft()
                self.delay_letter = 0

            self.win_text = self.font_large.render(f'{self.win_text_current}', True, (0, 0, 0))

        if self.cat.dead:
            self.delay_letter += 1

            if len(self.game_over_letters_queue) > 0 and self.delay_letter == 5:
                self.game_over_text_current += self.game_over_letters_queue.popleft()
                self.delay_letter = 0

            self.game_over_text = self.font_large.render(f'{self.game_over_text_current}', True, (0, 0, 0))

    def draw(self):
        self.screen.window.blit(self.cat_img, self.cat_rect)
        self.screen.window.blit(self.cat_lives_text, self.cat_lives_text_rect)
        self.screen.window.blit(self.fish_img, self.fish_rect)
        self.screen.window.blit(self.fish_text, self.fish_text_rect)
        self.screen.window.blit(self.score_text, self.score_text_rect)

        if self.dog.appear:
            self.screen.window.blit(self.dog_img, self.dog_rect)
            self.screen.window.blit(self.dog_lives_text, self.dog_lives_text_rect)

        if self.dog.dead:
            self.screen.window.blit(self.win_text, self.win_text_rect)

        if self.cat.dead:
            self.screen.window.blit(self.game_over_text, self.game_over_text_rect)
