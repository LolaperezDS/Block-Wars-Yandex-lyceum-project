from part import *
from sprites import *
from video_settings import *


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.x, self.y = x, y
        self.life, self.max_life = 9999, 9999
        self.image = None

    def get_coords(self):
        return self.x, self.y

    def get_image(self):
        return self.image


class PlayersObject(Object):
    def __init__(self, x, y, color, group):
        super().__init__(x, y, group)
        self.player = color
        self.x, self.y = x, y
        self.life, self.max_life = 9999, 9999
        self.image = None
        self.build_actions = 0
        self.to_be_built = 9999
        self.effect = 9999

    def is_built(self):
        return self.build_actions == self.to_be_built

    def build(self):
        if self.build_actions != self.to_be_built:
            self.build_actions = self.build_actions + 1
            if self.build_actions == self.to_be_built:
                self.life = self.max_life
        else:
            self.repair()

    def repair(self):
        self.life += 1
        if self.max_life < self.life:
            self.life = self.max_life


class TerrainObject(Object):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.x, self.y = x, y
        self.life = 9999
        self.one_resource = self.size // self.life
        self.image = None
        self.object_type = None
        self.size = 9999
        self.player = None

    def capture(self, player):
        self.player = player

    def resource(self):
        if self.player is not None:
            self.life -= 1
            self.player.add(self.object_type, self.one_resource)


class Player(pygame.sprite.Sprite):
    def __init__(self, group, color, name):
        super().__init__(group)
        self.color = color
        self.name = name
        self.max_actions = 3
        self.active = True
        self.actions = 3
        self.own = []
        self.resources = []

    def actions_update(self):
        count = 0
        for i in range(len(self.own)):
            game_object = self.own[i]
            if game_object.__class__ == Town and game_object.to_be_built == game_object.build_actions:
                count += 1
        self.max_actions = 3 + count // 3
        self.actions = self.max_actions

    def use_action(self):
        self.actions -= 1

    def add_own(self, objects):
        self.own.append(objects)


class Board:
    def __init__(self):
        self.turned_player = None
        self.players = None
        self.board = []
        self.DELTA = 100

        self.prepared = None
        self.choosed_gun = None

        self.delta_pos = (0, 0)

        self.cross_pos = (None, None)
        self.buildanim = AnimatedSprite(build_animation, 100)
        self.buildanim.activate()

        self.smoke = SmokeParticle(None, 400, 300, 5)
        self.fire = FireParticle(None, 200, 200, 3)

    def destroy_object(self, x, y):
        self.board[x][y] = None

    def set_up(self, players, player_index):
        self.turned_player = player_index
        self.players = players

    def render(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pos_x, pos_y = self.delta_pos[0] + i * self.DELTA, self.delta_pos[1] + j * self.DELTA
                if self.board[i][j] is not None:
                    image = self.board[i][j].image
                    block_image = None
                    for block in blocks:
                        if blocks[block] == self.board[i][j].player:
                            block_image = block
                    screen.blit(pygame.transform.scale(block_image.image, (self.DELTA, self.DELTA)),
                                (pos_x, pos_y))
                    if self.board[i][j].build_actions == self.board[i][j].to_be_built:
                        screen.blit(pygame.transform.scale(image, (self.DELTA, self.DELTA)),
                                    (pos_x, pos_y))
                        if self.board[i][j].__class__ == Town:
                            if self.board[i][j].life == 2:
                                self.smoke.sc = screen
                                self.smoke.update_pos(pos_x + self.DELTA // 2, pos_y + self.DELTA // 2)
                                self.smoke.action()
                            if self.board[i][j].life == 1:
                                self.fire.sc = screen
                                self.fire.update_pos(pos_x + self.DELTA // 2, pos_y + self.DELTA // 2)
                                self.fire.action()

                    else:
                        screen.blit(pygame.transform.scale(self.buildanim.image, (self.DELTA, self.DELTA)),
                                    (pos_x, pos_y))

                else:
                    if get_video_settings()[3] == 0:
                        pygame.draw.rect(screen, (0, 255, 0), (pos_x, pos_y, self.DELTA, self.DELTA))
                    else:
                        screen.blit(pygame.transform.scale(grass.image, (self.DELTA, self.DELTA)), (pos_x, pos_y))

    def crossing(self, pos):
        self.cross_pos = pos

    def render_crossing(self, screen):
        if self.cross_pos != (None, None):
            pos_x, pos_y = self.delta_pos[0] + self.cross_pos[0] * self.DELTA, self.delta_pos[1] + self.cross_pos[
                1] * self.DELTA
            pygame.draw.rect(screen, (0, 0, 0),
                             (pos_x, pos_y, self.DELTA, self.DELTA), 1)

    def camera_update(self, pos):
        temp_y, temp_x = -pos[0], -pos[1]
        if self.delta_pos[0] + temp_x <= pygame.display.Info().current_w - 300 - len(self.board) * self.DELTA:
            temp_x = 0
        if self.delta_pos[0] + temp_x >= 0:
            temp_x = 0
        if self.delta_pos[1] + temp_y <= pygame.display.Info().current_h - len(self.board[0]) * self.DELTA:
            temp_y = 0
        if self.delta_pos[1] + temp_y >= 0:
            temp_y = 0
        self.delta_pos = (self.delta_pos[0] + temp_x, self.delta_pos[1] + temp_y)

    def prepare_to_set_object(self, object_name):
        self.prepared = object_name

    def prepare_to_destroy_object(self):
        self.prepared = 'destroy'

    def get_click(self, mousepos):
        x, y = mousepos
        x1 = (x - self.delta_pos[0]) // self.DELTA
        y1 = (y - self.delta_pos[1]) // self.DELTA
        if x1 < len(self.board) and y1 < len(self.board[0]):
            return x1, y1
        else:
            return None, None

    def change_delta(self, integer):
        if self.DELTA + integer < 500:
            if (pygame.display.Info().current_w - 300) / len(self.board) < self.DELTA + integer:
                if pygame.display.Info().current_h / len(self.board[0]) < self.DELTA + integer:
                    self.DELTA += integer

    def possible(self, x, y, player):
        if 0 <= x - 1 < len(self.board[0]) and 0 <= y - 1 < len(self.board):
            pos = self.board[y - 1][x - 1]
            if check_possibility(pos, player):
                return True
            pos = self.board[y - 1][x]
            if check_possibility(pos, player):
                return True
            pos = self.board[y][x - 1]
            if check_possibility(pos, player):
                return True
        elif 0 <= x - 1 < len(self.board[0]):
            pos = self.board[y][x - 1]
            if check_possibility(pos, player):
                return True
        elif 0 <= y - 1 < len(self.board):
            pos = self.board[y - 1][x]
            if check_possibility(pos, player):
                return True
        if 0 <= x + 1 < len(self.board[0]) and 0 <= y + 1 < len(self.board):
            pos = self.board[y + 1][x + 1]
            if check_possibility(pos, player):
                return True
            pos = self.board[y + 1][x]
            if check_possibility(pos, player):
                return True
            pos = self.board[y][x + 1]
            if check_possibility(pos, player):
                return True
        elif 0 <= x + 1 < len(self.board[0]):
            pos = self.board[y][x + 1]
            if check_possibility(pos, player):
                return True
        elif 0 <= y + 1 < len(self.board):
            pos = self.board[y + 1][x]
            if check_possibility(pos, player):
                return True

        if 0 <= x - 1 < len(self.board[0]) and 0 <= y + 1 < len(self.board):
            pos = self.board[y + 1][x - 1]
            if check_possibility(pos, player):
                return True

        if 0 <= x + 1 < len(self.board[0]) and 0 <= y - 1 < len(self.board):
            pos = self.board[y - 1][x + 1]
            if check_possibility(pos, player):
                return True
        return False

    def on_screen(self, pos, screen_size):
        if screen_size[0] - 300 > pos[0]:
            return True

    def clear(self):
        pass


class MusicBox:
    def __init__(self, *tracks):
        self.value = 0.5
        self.tracks = list(tracks)
        self.value_update(self.value)

    def check(self):
        if not pygame.mixer.music.get_busy():
            self.play(random.choice(self.tracks))

    def play(self, track):
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(1)

    def add(self, track_path):
        self.tracks.append(track_path)

    def value_update(self, value):
        self.value = value
        pygame.mixer.music.set_volume(value)

    def playlist_init(self):
        files = os.listdir('data/sound/track/')
        tracks = filter(lambda x: x.endswith('.mp3'), files)
        for track in tracks:
            self.add('data/sound/track/' + track)


class Widget:
    def __init__(self, pos, text, pressed=False):
        self.x, self.y = pos
        self.pos = pos
        self.size = (None, None)
        self.pressed = pressed
        self.crossed = False
        self.text = text
        self.font = pygame.font.Font(None, 25)

    def press(self):
        self.pressed = True

    def crossing(self):
        if not self.pressed:
            self.crossed = True

    def check(self, mousepos):
        return crossing((self.x, self.y, self.size[0], self.size[1]), mousepos, full=True)

    def unpress(self):
        self.pressed = False


class Button(Widget):
    def __init__(self, pos, text, pressed=False, size=(250, 50)):
        super().__init__(pos, text, pressed=pressed)
        self.size = self.width, self.height = size[0], size[1]
        self.image_press = load_image_hud('button-clicked.png')
        self.image_nonpress = load_image_hud('button-nonclicked.png')

    def render(self, screen):
        if self.pressed:
            self.image = self.image_press
            color = (255, 255, 255)
        else:
            self.image = self.image_nonpress
            if self.crossed:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)
        screen.blit(self.image, self.pos)
        screen.blit(self.font.render(self.text, True, color), (self.pos[0] + 17, self.pos[1] + 17))


class CheckBox(Widget):
    def __init__(self, pos, text, pressed=False):
        super().__init__(pos, text, pressed=pressed)
        self.checked = pressed

    def render(self, screen):
        pass


class Slider(Widget):
    def __init__(self, pos, text, pressed=False, size=(400, 10)):
        super().__init__(pos, text, pressed=pressed)
        self.size = self.width, self.height = size
        self.xp = 200

    def get_pos(self):
        return self.xp / self.width

    def change_pos(self, mousepos):
        x = mousepos[0]
        if self.x <= x <= self.x + self.width:
            self.xp = x - self.x

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.pos[0], self.pos[1] + 20, self.width, self.height))
        if self.crossed:
            pygame.draw.circle(screen, (0, 0, 0), (self.pos[0] + self.xp, self.pos[1] + 25), 15)
            pygame.draw.circle(screen, (255, 255, 255), (self.pos[0] + self.xp, self.pos[1] + 25), 12)
        else:
            pygame.draw.circle(screen, (255, 255, 255), (self.pos[0] + self.xp, self.pos[1] + 25), 15)
            pygame.draw.circle(screen, (0, 0, 0), (self.pos[0] + self.xp, self.pos[1] + 25), 12)

    def check_circle(self, mousepos):
        if self.pos[0] + self.xp - 15 <= mousepos[0] <= self.pos[0] + self.xp + 15:
            if self.pos[1] + 25 - 15 <= mousepos[1] <= self.pos[1] + 25 + 15:
                return True
        return False


class Town(PlayersObject):
    def __init__(self, x, y, color, group, main_town=False):
        super().__init__(x, y, color, group)
        self.is_main_town = main_town
        self.max_life = 3 if not main_town else 6
        self.life = self.max_life
        self.build_actions = 0
        self.to_be_built = 3
        self.effect = 3
        self.image = main_town_sprite.image if self.is_main_town else town_sprite.image

    def change_image(self):
        self.image = main_town_sprite.image if self.is_main_town else town_sprite.image


class Gun(PlayersObject):
    def __init__(self, x, y, color, group):
        super().__init__(x, y, color, group)
        self.max_life = 2
        self.life = self.max_life
        self.build_actions = 0
        self.to_be_built = 2
        self.image = gun_sprite.image
        self.choosed = False
        self.angle = 6
        self.radius = 1
        self.effect = 1

    def change_image(self):
        self.image = gun_sprite.image

    def choose(self):
        self.choosed = True

    def unchoose(self):
        self.choosed = False

    def can_attack(self, pos):
        if abs(self.x - pos[0]) <= self.radius and abs(self.y - pos[1]) <= self.radius:
            return True
        return False


class Block(PlayersObject):
    def __init__(self, x, y, color, group):
        super().__init__(x, y, color, group)
        self.max_life = 1
        self.life = self.max_life
        self.build_actions = 0
        self.to_be_built = 1
        for color in blocks:
            if blocks[color] == self.player:
                self.image = color.image
        self.effect = 1

    def change_image(self):
        for color in blocks:
            if blocks[color] == self.player:
                self.image = color.image


class AnimatedSprite:
    def __init__(self, frames, max_counter, count=999):
        self.active = False
        self.count = 0
        self.max_counter = max_counter
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.max_count = count

    def update(self):
        if self.active:
            self.count += 1
            if self.count % self.max_counter == 0:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
            if self.max_count * self.max_counter * len(self.frames) == self.count:
                self.deactivate()

    def activate(self):
        self.active = True
        self.count = 0
        self.current_frame = 0

    def deactivate(self):
        self.active = False


class LoadLevelView:
    def __init__(self, levels, width, height, pos):
        self.levels = levels
        self.kol = height // 35
        self.height = height
        self.width = width
        self.x, self.y = pos
        self.view_levels = [None] * self.kol
        self.view_levels_pressed = [False] * self.kol
        self.view_levels_crossing = [False] * self.kol
        if len(self.levels) < self.kol:
            self.view_levels = [None] * len(self.levels)
            self.view_levels_pressed = [False] * len(self.levels)
            self.view_levels_crossing = [False] * len(self.levels)
        self.font = pygame.font.Font(None, 25)
        self.view_levels_setup()

    def view_levels_up(self):
        temp = self.view_levels.copy()
        for i in range(1, self.kol):
            self.view_levels[i] = temp[i - 1]
        self.view_levels[0] = self.levels[self.levels.index(temp[0]) - 1]
        self.view_levels_pressed = [False] * self.kol

    def view_levels_down(self):
        temp = self.view_levels.copy()
        for i in range(self.kol - 2, -1, -1):
            self.view_levels[i] = temp[i + 1]
        self.view_levels[self.kol - 1] = self.levels[self.levels.index(temp[self.kol - 1]) + 1]
        self.view_levels_pressed = [False] * self.kol

    def view_levels_update(self, screen):
        for i in range(len(self.view_levels)):
            level = self.view_levels[i]
            if self.view_levels_pressed[i]:
                pygame.draw.rect(screen, pygame.Color('white'), (self.x, self.y + i * 34, self.width, 34))
                color = pygame.Color('black')
            elif self.view_levels_crossing[i]:
                color = pygame.Color('white')
            else:
                color = pygame.Color('black')
            screen.blit(self.font.render(level, True, color), (self.x + 5, self.y + i * 34 + 7))

    def view_levels_setup(self):
        for i in range(self.kol):
            if len(self.levels) > i:
                self.view_levels[i] = self.levels[i]

    def crossing(self, mousepos):
        for i in range(len(self.view_levels)):
            if crossing((self.x, self.y + i * 34, self.width, 34), mousepos, full=True):
                self.view_levels_crossing[i] = True
                return i
            else:
                self.view_levels_crossing[i] = False
        return None

    def press(self, x):
        self.view_levels_pressed[x] = True

    def unpress(self):
        self.view_levels_pressed = [False] * self.kol


class Hud:
    def __init__(self, window_size):
        self.window_size = self.width, self.height = window_size
        self.turn_text = 'Turn: Player 1'
        self.actions_text = 'Actions left: 1'
        self.actions_left = ''
        self.actions = 1
        self.info_name = 'Name: '
        self.info_health = 'Health: '
        self.pos = (self.width - 300, self.height)
        self.font = pygame.font.Font(None, 25)

        self.colors = [pygame.Color('red'), pygame.Color('blue'), pygame.Color('green'), pygame.Color('yellow')]
        self.color_mode = pygame.Color('red')

    def update_hud(self, sc):
        pygame.draw.rect(sc, (40, 40, 40), (self.pos[0], 0, 300, self.pos[1]))
        sc.blit(self.font.render(self.turn_text, True, (255, 255, 255)), (self.pos[0] + 25, 270))
        sc.blit(self.font.render(self.actions_text, True, (255, 255, 255)), (self.pos[0] + 25, 290))
        self.actions_left = 'Actions to build over: '

    def set_turned_text(self, player_name, player):
        self.turn_text = player_name
        self.actions_text = 'Actions left: ' + str(player.max_actions)
        self.actions = player.max_actions
        self.color_mode = player.color

    def update_actions(self):
        self.actions -= 1
        self.actions_text = 'Actions left: ' + str(self.actions)

    def draw_info(self, pos, sc, item):
        if item is not None:
            info_x, info_y = pos
            if info_x != -1 and info_y != -1:
                for i in range(1, 11):
                    if i <= (item.life / item.max_life) * 10:
                        color = pygame.Color('green')
                    else:
                        color = pygame.Color('red')
                    pygame.draw.rect(sc, color, (self.pos[0] + 140 + (i - 1) * 10, 330, 10, 17), 0)
                image_color = None
                for colors in blocks:
                    if blocks[colors] == item.player:
                        image_color = colors.image
                        break
                image = pygame.transform.scale(item.image, (50, 50))
                image_2 = pygame.transform.scale(image_color, (50, 50))
                sc.blit(self.font.render(self.info_name + item.__class__.__name__, True, (255, 255, 255)),
                        (self.pos[0] + 80, 310))
                sc.blit(self.font.render(self.info_health, True, (255, 255, 255)), (self.pos[0] + 80, 330))
                sc.blit(self.font.render(str(item.life), True, (0, 0, 0)), (self.pos[0] + 185, 330))
                sc.blit(image_2, (self.pos[0] + 25, 310))
                sc.blit(image, (self.pos[0] + 25, 310))
                if not item.is_built:
                    sc.blit(self.font.render(self.actions_left + str(item.to_be_built - item.build_actions), True,
                                             (255, 255, 255)), (self.pos[0] + 80, 350))


def load_level(filename):
    f = open(filename)
    colors = [pygame.Color('red'), pygame.Color('blue'), pygame.Color('yellow'), pygame.Color('green')]
    alldata = f.readlines()

    board = []
    temp_board = []

    players = []
    alldata.pop(0)
    first_player = int(alldata.pop(-1).strip())

    for i in range(len(alldata)):
        string = alldata[i].strip()
        for j in range(len(string.split(';'))):
            tmp = string.split(';')[j]
            if tmp != '.':
                if tmp[0] == '@':
                    cur_player = None
                    for player in players:
                        if colors[int(tmp[1]) - 1] == player.color:
                            cur_player = player
                    if not cur_player:
                        cur_player = Player(all_sprites, colors[int(tmp[1]) - 1], 'Player ' + tmp[1])
                        players.append(cur_player)
                    temp_board.append(Town(i, j, cur_player.color, all_sprites, main_town=True))
                    cur_player.add_own(temp_board[-1])
                if tmp[0] == 'T':
                    cur_player = None
                    for player in players:
                        if colors[int(tmp[1]) - 1] == player.color:
                            cur_player = player
                    if not cur_player:
                        cur_player = Player(all_sprites, colors[int(tmp[1]) - 1], 'Player ' + tmp[1])
                        players.append(cur_player)
                    temp_board.append(Town(i, j, cur_player.color, all_sprites))
                    cur_player.add_own(temp_board[-1])
                if tmp[0] == 'G':
                    cur_player = None
                    for player in players:
                        if colors[int(tmp[1]) - 1] == player.color:
                            cur_player = player
                    if not cur_player:
                        cur_player = Player(all_sprites, colors[int(tmp[1]) - 1], 'Player ' + tmp[1])
                        players.append(cur_player)

                    temp_board.append(Gun(i, j, cur_player.color, all_sprites))
                    cur_player.add_own(temp_board[-1])
                if tmp[0] == 'B':
                    cur_player = None
                    for player in players:
                        if colors[int(tmp[1]) - 1] == player.color:
                            cur_player = player
                    if not cur_player:
                        cur_player = Player(all_sprites, colors[int(tmp[1]) - 1], 'Player ' + tmp[1])
                        players.append(cur_player)
                    temp_board.append(Block(i, j, cur_player.color, all_sprites))
                    cur_player.add_own(temp_board[-1])
                if tmp.split('*')[1] == 'b':
                    temp_board[-1].build_actions = temp_board[-1].to_be_built
                else:
                    temp_board[-1].build_actions = int(tmp.split('*')[1])
                if tmp.split('*')[2] != 'd':
                    temp_board[-1].life = int(tmp.split('*')[2])
            else:
                temp_board.append(None)
        board.append(temp_board.copy())
        temp_board = []
        for p in players:
            p.active = True
    return board, players, players[first_player - 1]


class Mouse:
    def __init__(self):

        self.default_image = mouse.image
        self.town_image = pygame.transform.scale(town_sprite.image, (20, 20))
        self.gun_image = pygame.transform.scale(gun_sprite.image, (20, 20))
        self.destroy_image = destroy_sprite.image
        self.current_player = None
        self.block_image = pygame.transform.scale(redblock.image, (20, 20))

        self.blocks_image = [(pygame.Color('red'), redblock.image), (pygame.Color('blue'), blueblock.image),
                             (pygame.Color('green'), greenblock.image), (pygame.Color('yellow'), yellowblock.image)]

        self.pos = (0, 0)
        self.mode = None

    def change_pos(self, pos):
        self.pos = pos

    def render(self, screen):
        if self.block_image is not None and self.mode != self.destroy_image and \
                self.mode != self.default_image and self.mode is not None:
            screen.blit(self.block_image, (self.pos[0] + 10, self.pos[1] + 10))
        if self.mode is not None:
            screen.blit(self.mode, (self.pos[0] + 10, self.pos[1] + 10))
        screen.blit(self.default_image, self.pos)

    def change_mode(self, object_name):
        if object_name == 'Town':
            self.mode = self.town_image
        elif object_name == 'Gun':
            self.mode = self.gun_image
        elif object_name == 'Default':
            self.mode = None
        elif object_name == 'Destroy':
            self.mode = self.destroy_image
        elif object_name == 'Block':
            self.mode = self.block_image

    def changed_turn(self, player):
        self.current_player = player
        for block in self.blocks_image:
            if player.color == block[0]:
                cur_player_block = pygame.transform.scale(block[1], (20, 20))
        self.block_image = cur_player_block


def check_possibility(pos, player):
    if pos is not None and pos.player == player:
        if pos.__class__.__name__ == 'Town':
            return True
        if pos.__class__.__name__ == 'Block':
            return True
    return False


class Message:
    def __init__(self, text, pos, color, count, default=True):
        self.pos = pos
        self.color = color
        self.max_count = count
        self.font = pygame.font.Font(None, 25)
        self.text = text
        self.count = 0
        self.active = False
        self.default = default

    def render(self, screen):
        if self.active and self.count <= self.max_count:
            screen.blit(self.font.render(self.text, True, self.color), self.pos)
            self.count += 1

    def activate(self):
        self.active = True
        self.to_vanish = False
        self.count = 0
