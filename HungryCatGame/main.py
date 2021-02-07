from random import randint

import pygame

from background import Background
from button import Button
from game import Game
from screen import Screen

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

pygame.init()
screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_caption('Hungry Cat')

clock = pygame.time.Clock()

ADDDOGATTACK = pygame.USEREVENT + 1

bg = Background(screen)

game = Game(screen, bg, ADDDOGATTACK)

resume_button = Button(screen, 'RESUME', 150)
new_game_button = Button(screen, 'NEW GAME', 210)
credits_button = Button(screen, 'CREDITS', 270)
quit_button = Button(screen, 'QUIT GAME', 330)

buttons_group = [new_game_button, credits_button, quit_button]
selected_button_idx = 0

menu = True
show_credits = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and menu:
                selected_button_idx += 1
                if selected_button_idx >= len(buttons_group):
                    selected_button_idx = 0

            elif event.key == pygame.K_UP and menu:
                selected_button_idx -= 1
                if selected_button_idx < 0:
                    selected_button_idx = len(buttons_group) - 1

            elif event.key == pygame.K_RETURN and menu:
                menu = False

                if buttons_group[selected_button_idx].text.lower() == 'new game':
                    if resume_button not in buttons_group:
                        buttons_group.insert(0, resume_button)

                    bg = Background(screen)

                    game = Game(screen, bg, ADDDOGATTACK)

                elif buttons_group[selected_button_idx].text.lower() == 'credits':
                    show_credits = True

                elif buttons_group[selected_button_idx].text.lower() == 'quit game':
                    run = False

                selected_button_idx = 0

            elif event.key == pygame.K_ESCAPE:
                menu = True
                show_credits = False

        if event.type == ADDDOGATTACK:
            game.dog.attack = True
            pygame.time.set_timer(ADDDOGATTACK, randint(1000, 3000))

    pressed_keys = pygame.key.get_pressed()

    bg.draw()

    if menu:
        for btn in buttons_group:
            btn.draw()

        buttons_group[selected_button_idx].draw_border()

    elif show_credits:
        credits_img = pygame.image.load('images/credits.png').convert()
        screen.window.blit(credits_img, (0, 0))

    elif run:
        game.game_loop(pressed_keys)

    if not show_credits:
        game.game_info.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
