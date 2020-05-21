import pygame
import classes, sprites, game, fun

pygame.init()

FPS = 120
width = 1200
height = 800
volume = 0.5


def new_game_choose(width, height, fullscreen):
    running = True
    x, y, a, b = 0, 0, 0, 0
    FPS = 60
    choosen = '.'
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(0)
    screen_2 = pygame.display.set_mode((width, height), fullscreen)

    button_choose_map = classes.Button((int(width * 3 / 4) - classes.Button.size[1], int(height * 3 / 4)), 'Choose Map')
    button_back = classes.Button((width // 4, int(height * 3 / 4)), 'Back')
    buttons = [button_choose_map, button_back]
    levels = sprites.levels
    choose_text = 'Choose Level'
    font = classes.FONT
    i = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEMOTION:
                a, b = event.pos
                for button in buttons:
                    button.crossing(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button in buttons:
                    if button.crossing((x, y)):
                        choosen = button.press()
                if choosen == 'Choose Map':
                    return levels[i].text
                if choosen == 'Back':
                    running = False
                if fun.crossing((width // 4, height // 2), (x, y)):
                    if i != 0:
                        i -= 1
                if fun.crossing((int((width * 3) / 4) - 25, height // 2), (x, y)):
                    if i != len(sprites.levels) - 1:
                        i += 1
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    button.unpress()
        # screen.blit(image, (0, 0))
        screen_2.fill((40, 40, 40))
        screen_2.fill((100, 100, 100), (width // 4, height // 4, width // 2, height // 2))
        screen_2.blit(font.render(choose_text, True, pygame.Color('white')), (width // 2 - 50, height // 4 + 17))
        screen_2.blit(levels[i].image, (width // 4 + 25, height // 4 + 50))
        if i != 0:
            screen_2.blit(sprites.left.image, (width // 4, height // 2))
        if i != len(sprites.levels) - 1:
            screen_2.blit(sprites.right.image, (int((width * 3) / 4) - 25, height // 2))
        for button in buttons:
            button.render(screen_2)
        if pygame.mouse.get_focused():
            screen_2.blit(sprites.mouse.image, (a, b))
        pygame.display.flip()
        clock.tick(FPS)
