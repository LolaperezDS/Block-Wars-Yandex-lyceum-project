import pygame, os

from classes import *
from sprites import *
from fun import *
from game import *

pygame.init()

FPS = 120
width = 1200
height = 800
volume = 0.5


def load_game_choose(width, height, screen, arrow, music_box):
    running = True
    x, y, a, b = 0, 0, 0, 0
    FPS = 60
    choosen = '.'
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(0)

    button_start_game = Button((int(width * 3 / 4) - 250, int(height * 3 / 4)), 'Start Game')
    button_back = Button((width // 4, int(height * 3 / 4)), 'Back')
    buttons = [button_start_game, button_back]

    choose_text = 'Choose Level'
    choosed_level = ''
    levels = find_levels()
    view_levels = LoadLevelView(levels, width // 2 - 10, height // 2 - 75, (width // 4 + 5, height // 4 + 75))
    i, j = 0, 0
    left_bool, right_bool, view_bool = False, False, False
    font = pygame.font.Font(None, 25)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                for button in buttons:
                    if button.check((mouse_x, mouse_y)):
                        button.crossing()
                    else:
                        button.crossed = False
                arrow.change_pos(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.check(event.pos):
                        button.press()
                        choosen = button.text.strip()

                if crossing((width // 2, height // 4 + 40), event.pos):
                    left_bool = True
                if crossing((width // 2, int((height * 3) / 4) - 25), event.pos):
                    right_bool = True
                x = view_levels.crossing(event.pos)
                if x is not None:
                    view_bool = True
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.check(event.pos) and button.pressed:
                        if choosen == 'Start Game':
                            if choosed_level != '':
                                fullname = os.path.join('data/saves/' + choosed_level)
                                game(width, height, screen, arrow, music_box, fullname)
                                running = False
                        if choosen == 'Back':
                            running = False

                if crossing((width // 2, height // 4 + 40), event.pos) and left_bool:
                    if j != 0:
                        view_levels.view_levels_up()
                        j -= 1
                        if i != 0:
                            i -= 1
                if crossing((width // 2, int((height * 3) / 4) - 25), event.pos) and right_bool:
                    if j + view_levels.kol < len(view_levels.levels):
                        view_levels.view_levels_down()
                        j += 1
                        if i != view_levels.kol - 1:
                            i += 1
                x = view_levels.crossing(event.pos)
                if x is not None and view_bool:
                    view_levels.press(x)
                    choosed_level = view_levels.view_levels[x]
                    for i in range(len(view_levels.view_levels)):
                        if view_levels.view_levels[i] != view_levels.view_levels[x]:
                            view_levels.view_levels_pressed[i] = False
                else:
                    choosed_level = ''

                left_bool, right_bool, view_bool = False, False, False
                for button in buttons:
                    button.unpress()

        screen.fill((40, 40, 40))
        screen.fill((100, 100, 100), (width // 4, height // 4, width // 2, height // 2))
        screen.blit(font.render(choose_text, True, pygame.Color('white')), (width // 2 - 50, height // 4 + 17))
        if j != 0:
            screen.blit(up.image, (width // 2, height // 4 + 40))
        if j + view_levels.kol < len(view_levels.levels) and len(view_levels.levels) > view_levels.kol:
            screen.blit(down.image, (width // 2, int((height * 3) / 4) - 25))
        for button in buttons:
            button.render(screen)
        view_levels.view_levels_update(screen)
        arrow.render(screen)
        music_box.check()
        pygame.display.flip()
        clock.tick(FPS)
