import pygame
from classes import *
from fun import *
from sprites import *
from new_game_choose import new_game_choose
from settings import settings
from load_game_choose import load_game_choose
from video_settings import *

pygame.init()

size, volume, fullscreen, graphics, FPS = load_settings()
SIZE, VOLUME, FULLSCREEN, GRAPHICS, FPS_GLOBAL = size, volume, fullscreen, graphics, FPS
video_settings_init(size, volume, fullscreen, graphics, FPS)

running = True
mouse_x, mouse_y = 0, 0
choosen = '.'

width, height = size

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height), fullscreen)
pygame.display.set_caption('BlockWars')

pygame.mouse.set_visible(0)
arrow = Mouse()

music_box = MusicBox()
music_box.playlist_init()
music_box.value_update(volume)
music_box.check()

button_newgame = Button((width // 2 - 125, height // 2 - 50), 'New Game')
button_loadgame = Button((width // 2 - 125, height // 2 + 70 - 50), 'Load Game')
button_multiplayer = Button((width // 2 - 125, height // 2 + 140 - 50), 'Multiplayer')
button_settings = Button((width // 2 - 125, height // 2 + 210 - 50), 'Settings')
button_exit = Button((width // 2 - 125, height // 2 + 280 - 50), 'Exit')
buttons = [button_newgame, button_loadgame, button_multiplayer, button_settings, button_exit]

BW_image = pygame.transform.scale(BW.image, (width // 2, height // 4))

fire_for_logo = FireParticle(screen, width // 4 + width // 16 + width // 16, height // 8 + 20, 5)

coming_soon_message = Message('Coming Soon', (width // 2 - width // 20, (height * 7) // 8), (255, 255, 255), 10000)

for lvl_preview in levels:
    lvl_preview.image = pygame.transform.scale(lvl_preview.image, (width // 2 - 50, height // 2 - 50))

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
                if button.check(event.pos):
                    button.press()
                    choosen = button.text.strip()
        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                if button.check(event.pos) and button.pressed:
                    if choosen == 'Settings':
                        settings(width, height, screen, arrow, music_box)
                    if choosen == 'Exit':
                        running = False
                    if choosen == 'New Game':
                        new_game_choose(width, height, screen, arrow, music_box)
                    if choosen == 'Load Game':
                        load_game_choose(width, height, screen, arrow, music_box)
                    if choosen == 'Multiplayer':
                        coming_soon_message.activate()
                    choosen = '.'
                button.unpress()
            choosen = '.'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if fullscreen:
                    screen = pygame.display.set_mode((width, height))
                else:
                    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                fullscreen = not fullscreen
    screen.fill((40, 40, 40))
    screen.blit(BW_image, (width // 4 + width // 16, height // 8))
    for button in buttons:
        button.render(screen)
    if pygame.mouse.get_focused():
        arrow.render(screen)
    coming_soon_message.render(screen)
    music_box.check()
    fire_for_logo.action()
    pygame.display.flip()
    clock.tick(FPS)
