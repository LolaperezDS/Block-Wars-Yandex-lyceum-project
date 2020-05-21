import os, pygame

pygame.init()


def load_image(name, colorkey=pygame.Color('brown')):
    fullname = os.path.join('data/sprites', name)
    image = pygame.image.load(fullname)
    image.set_colorkey(colorkey)
    return image


def load_image_hud(name):
    fullname = os.path.join('data/HUD_sprites', name)
    image = pygame.image.load(fullname)
    return image


def save_game(x, name_file=''):
    if name_file == '':
        a = 0
        while a > -1:
            try:
                open('data/saves/saved_game' + str(a) + '.txt', 'r')
            except BaseException:
                break
            else:
                a += 1
        fullname = os.path.join('data/saves/saved_game' + str(a) + '.txt')
        file = open(fullname, 'w')
        file.write(x)
        file.close()
    else:
        fullname = os.path.join('data/saves/{}.txt'.format(name_file))
        file = open(fullname, 'w')
        file.write(x)
        file.close()


def crossing(pos, mousepos, full=False):
    x1, y1 = mousepos
    x2, y2, w2, h2 = pos[0], pos[1], 25, 25
    if full:
        x2, y2, w2, h2 = pos[0], pos[1], pos[2], pos[3]
    if x2 <= x1 <= x2 + w2 and y2 <= y1 <= y2 + h2:
        return True
    return False


def get_color(x):
    if x == 1:
        return pygame.Color('blue')
    elif x == 2:
        return pygame.Color('red')
    elif x == 3:
        return pygame.Color('yellow')
    elif x == 4:
        return pygame.Color('green')


def load_settings():
    screen_size = (1200, 800)
    volume = 0.5
    fullscreen = 0
    graphics = 0
    fps = 120
    try:
        open('data/settings/saved_settings.txt', 'r')
    except BaseException:
        f = open('data/settings/default_settings.txt', 'r')
    else:
        f = open('data/settings/saved_settings.txt', 'r')
    for i in f:
        data = i.split('=')
        if data[0] == 'screen':
            screen_size = tuple(map(int, data[1].strip().split(';')))
        if data[0] == 'volume':
            volume = float(data[1].strip())
        if data[0] == 'fullscreen' and data[1].strip() == 'True':
            fullscreen = pygame.FULLSCREEN
        if data[0] == 'graphics':
            graphics = int(data[1])
            print(data[1])
        if data[0] == 'fps':
            fps = int(data[1])
    return screen_size, volume, fullscreen, graphics, fps


def save_settings(screen, volume, fullscreen, graphics, fps):
    f = open('data/settings/saved_settings.txt', 'w')
    f.write("screen={};{}\nvolume={}\nfullscreen={}\ngraphics={}\nfps={}".format(screen[0], screen[1],
                                                                                 volume, fullscreen, graphics, fps))
    f.close()


def find_levels():
    fullname = os.path.join('data/saves/')
    files = os.listdir(fullname)
    levels = list(filter(lambda x: x.endswith('.txt'), files))
    return levels


def win(c, sc, w, h):
    clock = pygame.time.Clock()
    running = True
    f = pygame.font.Font(None, 70)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        pygame.draw.rect(sc, c, (0, 0, w, h))
        sc.blit(f.render('WIN', True, (255, 255, 255)), (w // 2 - 70, h // 2 - 70))
        pygame.display.flip()
        clock.tick(60)
