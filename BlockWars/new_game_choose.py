import pygame
from classes import *
from sprites import *
from fun import *
from game import *

# from game_2 import *

pygame.init()

FPS = 120
width = 1200
height = 800
volume = 0.5


def new_game_choose(width, height, screen, arrow, music_box):
    running = True
    x, y, mouse_x, mouse_y = 0, 0, 0, 0
    FPS = 60
    choosen = '.'
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(0)

    button_start_game = Button((int(width * 3 / 4) - 250, int(height * 3 / 4)), 'Start Game')
    button_back = Button((width // 4, int(height * 3 / 4)), 'Back')
    buttons = [button_start_game, button_back]
    choose_text = 'Choose Level'
    i = 0

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
                x, y = event.pos
                for button in buttons:
                    if button.check((x, y)):
                        button.press()
                        choosen = button.text
                if crossing((width // 4, height // 2), (x, y)):
                    if i != 0:
                        i -= 1
                if crossing((int((width * 3) / 4) - 25, height // 2), (x, y)):
                    if i != len(levels) - 1:
                        i += 1
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.check(event.pos) and button.pressed:
                        if choosen == 'Start Game':
                            game(width, height, screen, arrow, music_box, levels[i].text)
                            running = False
                        if choosen == 'Back':
                            running = False
                for button in buttons:
                    button.unpress()
        screen.fill((40, 40, 40))
        screen.fill((100, 100, 100), (width // 4, height // 4, width // 2, height // 2))
        screen.blit(font.render(choose_text, True, pygame.Color('white')), (width // 2 - 50, height // 4 + 17))
        screen.blit(levels[i].image, (width // 4 + 25, height // 4 + 50))
        if i != 0:
            screen.blit(left.image, (width // 4, height // 2))
        if i != len(levels) - 1:
            screen.blit(right.image, (int((width * 3) / 4) - 25, height // 2))
        for button in buttons:
            button.render(screen)
        if pygame.mouse.get_focused():
            arrow.render(screen)
        music_box.check()
        pygame.display.flip()
        clock.tick(FPS)
