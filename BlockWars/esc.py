import pygame
from sprites import *
from classes import *
from fun import *
from settings import *

pygame.init()


def menu(width, height, screen, arrow, music_box, board):
    running = True
    x, y, a, b = 0, 0, 0, 0
    FPS = 120
    choosen = '.'
    clock = pygame.time.Clock()

    button_continue = Button((5, height - 205), 'Continue')
    button_save = Button((5, height - 155), 'Save Game')
    button_settings = Button((5, height - 105), 'Settings')
    button_exit = Button((5, height - 55), 'Exit')
    buttons = [button_continue, button_save, button_settings, button_exit]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.check(event.pos):
                        button.crossing()
                    else:
                        button.crossed = False
                arrow.change_pos(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.check(event.pos):
                        button.press()
                        choosen = button.text
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.check(event.pos) and button.pressed:
                        if choosen == 'Continue':
                            return True
                        if choosen == 'Save Game':
                            x, y = len(board.board[0]), len(board.board)
                            data = ''
                            data_1 = '{} {}\n'.format(x, y)
                            data_2 = [['.'] * x for i in range(y)]
                            data_3 = str(colors.index(board.turned_player.color) + 1)
                            for i in range(y):
                                for j in range(x):
                                    if board.board[i][j] is not None:
                                        if board.board[i][j].__class__ == Town:
                                            if board.board[i][j].is_main_town:
                                                data_2[i][j] = '@'
                                            else:
                                                data_2[i][j] = 'T'
                                        if board.board[i][j].__class__ == Gun:
                                            data_2[i][j] = 'G'
                                        if board.board[i][j].__class__ == Block:
                                            data_2[i][j] = 'B'
                                        data_2[i][j] += str(colors.index(board.board[i][j].player) + 1) + '*' \
                                                        + str(board.board[i][j].build_actions) + '*' \
                                                        + str(board.board[i][j].life)
                                for j in range(1, x):
                                    data_2[i][0] += ';' + data_2[i][j]
                            data += data_1
                            for i in range(len(data_2)):
                                data += data_2[i][0] + '\n'
                            data += data_3
                            save_game(data)
                        if choosen == 'Settings':
                            settings(width, height, screen, arrow, music_box)
                        if choosen == 'Exit':
                            running = False
                for button in buttons:
                    button.unpress()
        screen.fill((50, 50, 50))
        board.render(screen)
        for button in buttons:
            button.render(screen)
        arrow.render(screen)
        music_box.check()
        pygame.display.flip()
        clock.tick(FPS)
