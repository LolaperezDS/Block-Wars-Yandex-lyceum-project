import pygame
from classes import *
from sprites import *
from fun import *
from video_settings import get_video_settings, video_settings_init

pygame.init()


def settings(width, height, screen, arrow, music_box):
    SIZE, VOLUME, FULLSCREEN, GRAPHICS, FPS_GLOBAL = get_video_settings()
    running = True
    FPS = FPS_GLOBAL
    width, height = SIZE[0], SIZE[1]
    choosen = '.'
    clock = pygame.time.Clock()

    volume_slider = Slider((20, 80), 'volume')
    fps_slider = Slider((20, 330), 'fps')

    button_exit = Button((5, height), 'Back')
    button_save_settings = Button((width, height), 'Save Setting')
    button_exit = Button((20, height - 70), 'Back')
    button_save_settings = Button((width - 270, height - 70), 'Save Setting')
    button_gr_0 = Button((20, 170), 'low')
    button_gr_1 = Button((20, 220), 'high')

    button_r_1920_1080 = Button((500, 70), '1920x1080')
    button_r_1680_1024 = Button((500, 120), '1680x1024')
    button_r_1200_800 = Button((500, 170), '1200x800')
    button_r_1024_768 = Button((500, 220), '1024x768')
    button_r_640_480 = Button((500, 270), '640x480')
    button_fullscreen = Button((500, 320), 'fullscreen')
    buttons = [button_exit, button_save_settings, button_gr_0, button_gr_1, button_r_1680_1024, button_r_640_480,
               button_r_1024_768, button_r_1920_1080, button_r_1200_800, button_fullscreen]
    sliders = [volume_slider, fps_slider]

    restart_message = Message('Restart the game for the changes to take effect', (400, 750), (255, 255, 255), 10000)

    volume_slider.change_pos([int(VOLUME * volume_slider.width) + volume_slider.pos[0], None])
    fps_slider.change_pos([int(((FPS - 20) / 100) * fps_slider.width + fps_slider.pos[0]), None])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.check(event.pos):
                        button.crossing()
                    else:
                        button.crossed = False
                for slider in sliders:
                    if slider.pressed:
                        slider.change_pos(event.pos)
                        if slider.text == 'volume':
                            music_box.value_update(slider.get_pos())
                            VOLUME = slider.get_pos()
                        elif slider.text == 'fps':
                            FPS_GLOBAL = int(slider.get_pos() * 100 // 1 + 20)
                    if slider.check_circle(event.pos):
                        slider.crossing()
                    else:
                        slider.crossed = False
                arrow.change_pos(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.check(event.pos):
                        button.press()
                        choosen = button.text
                for slider in sliders:
                    if slider.check_circle(event.pos):
                        slider.press()
                    if slider.check(event.pos):
                        if slider.text == 'volume':
                            slider.change_pos(event.pos)
                            music_box.value_update(slider.get_pos())
                            VOLUME = slider.get_pos()
                        elif slider.text == 'fps':
                            slider.change_pos(event.pos)
                            FPS_GLOBAL = int(slider.get_pos() * 100 // 1 + 20)
                        slider.press()
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.check(event.pos) and button.pressed:
                        if choosen == 'Back':
                            running = False
                        if choosen == 'Save Setting':
                            save_settings(SIZE, VOLUME, FULLSCREEN, GRAPHICS, FPS_GLOBAL)
                            video_settings_init(SIZE, VOLUME, FULLSCREEN, GRAPHICS, FPS_GLOBAL)
                            restart_message.activate()
                        if choosen == 'low':
                            GRAPHICS = 0
                        if choosen == 'high':
                            GRAPHICS = 1
                        if choosen == 'fullscreen':
                            FULLSCREEN = True
                        if 'x' in choosen:
                            FULLSCREEN = False
                            WIDTH, HEIGHT = map(int, choosen.split('x'))
                            SIZE = (WIDTH, HEIGHT)
                        choosen = '.'
                    button.unpress()
                for slider in sliders:
                    slider.unpress()
        screen.fill((50, 50, 50))
        screen.blit(font.render('Settings', True, (255, 255, 255)), (20, 20))
        screen.blit(font.render('Music', True, (255, 255, 255)), (20, 60))
        screen.blit(font.render('Graphics', True, (255, 255, 255)), (20, 150))
        screen.blit(font.render('FPS', True, (255, 255, 255)), (20, 310))
        screen.blit(font.render(str(int(fps_slider.get_pos() * 100 // 1 + 20)), True, (255, 255, 255)), (100, 310))
        screen.blit(font.render('Screen resolution', True, (255, 255, 255)), (500, 20))
        for button in buttons:
            button.render(screen)
        for slider in sliders:
            slider.render(screen)
        restart_message.render(screen)
        arrow.render(screen)
        music_box.check()
        pygame.display.flip()
        clock.tick(FPS)
