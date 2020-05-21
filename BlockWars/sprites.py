import pygame
from fun import *

pygame.init()

all_sprites = pygame.sprite.Group()
gun_sprite_group = pygame.sprite.Group()
block_sprite_group = pygame.sprite.Group()
town_sprite_group = pygame.sprite.Group()

font = pygame.font.Font(None, 25)

build_animation = [pygame.image.load('data/animations/BuildAnim/untildone_1.png'),
                   pygame.transform.rotate(pygame.image.load('data/animations/BuildAnim/untildone_1.png'), 90)]

gun_sprite = pygame.sprite.Sprite()
gun_sprite.image = pygame.transform.scale(load_image('gun.png'), (100, 100))

BW = pygame.sprite.Sprite()
BW.image = load_image('BW_all.png')
colorkey = BW.image.get_at((0, 0))
BW.image.set_colorkey(colorkey)

right = pygame.sprite.Sprite()
right.image = load_image('left.png')

left = pygame.sprite.Sprite()
left.image = pygame.transform.rotate(right.image, 180)

up = pygame.sprite.Sprite()
up.image = pygame.transform.rotate(right.image, 90)

down = pygame.sprite.Sprite()
down.image = pygame.transform.rotate(right.image, 270)

mouse = pygame.sprite.Sprite()
mouse.image = load_image_hud('arrow.png')

block_sprite = pygame.sprite.Sprite()
board_sprite = pygame.sprite.Sprite()

town_sprite = pygame.sprite.Sprite()
town_sprite.image = pygame.transform.scale(load_image('town.png'), (100, 100))

destroy_sprite = pygame.sprite.Sprite()
destroy_sprite.image = load_image_hud('grave.png')

main_town_sprite = pygame.sprite.Sprite()
main_town_sprite.image = pygame.transform.scale(load_image('main_town.png'), (100, 100))

redblock = pygame.sprite.Sprite()
redblock.image = pygame.transform.scale(load_image('redblock.png'), (100, 100))

blueblock = pygame.sprite.Sprite()
blueblock.image = pygame.transform.scale(load_image('blueblock.png'), (100, 100))

yellowblock = pygame.sprite.Sprite()
yellowblock.image = pygame.transform.scale(load_image('yellowblock.png'), (100, 100))

greenblock = pygame.sprite.Sprite()
greenblock.image = pygame.transform.scale(load_image('greenblock.png'), (100, 100))

bloom_sprite = pygame.sprite.Sprite()
bloom_sprite.image = pygame.image.load('data/sprites/bloom.png')

grass = pygame.sprite.Sprite()
grass.image = pygame.transform.scale(load_image('grass.png'), (100, 100))

blocks = {redblock: pygame.Color('red'), blueblock: pygame.Color('blue'), yellowblock: pygame.Color('yellow'),
          greenblock: pygame.Color('green')}

colors = [pygame.Color('red'), pygame.Color('blue'), pygame.Color('yellow'), pygame.Color('green')]

sprite = [main_town_sprite, town_sprite, gun_sprite, blueblock, redblock, greenblock, yellowblock]

newturnanim = [pygame.image.load('data/animations/NewTurnAnim/anim_1.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_2.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_3.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_4.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_5.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_6.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_7.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_8.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_9.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_10.png')]

lvl_1_2 = pygame.sprite.Sprite()
lvl_1_3 = pygame.sprite.Sprite()
lvl_1_4 = pygame.sprite.Sprite()
lvl_2_2 = pygame.sprite.Sprite()
lvl_2_3 = pygame.sprite.Sprite()
lvl_2_4 = pygame.sprite.Sprite()

lvl_1_2.image = pygame.image.load('data/levels/lvlpreview/lvl_1_2.png')
lvl_1_3.image = pygame.image.load('data/levels/lvlpreview/lvl_1_3.png')
lvl_1_4.image = pygame.image.load('data/levels/lvlpreview/lvl_1_4.png')
lvl_2_2.image = pygame.image.load('data/levels/lvlpreview/lvl_2_2.png')
lvl_2_3.image = pygame.image.load('data/levels/lvlpreview/lvl_2_3.png')
lvl_2_4.image = pygame.image.load('data/levels/lvlpreview/lvl_2_4.png')

lvl_1_2.text = 'data/levels/lvl_1_2.txt'
lvl_1_3.text = 'data/levels/lvl_1_3.txt'
lvl_1_4.text = 'data/levels/lvl_1_4.txt'
lvl_2_2.text = 'data/levels/lvl_2_2.txt'
lvl_2_3.text = 'data/levels/lvl_2_3.txt'
lvl_2_4.text = 'data/levels/lvl_2_4.txt'

levels = [lvl_1_2, lvl_1_3, lvl_1_4, lvl_2_2, lvl_2_3, lvl_2_4]

click = pygame.mixer.Sound('data/sound/oneshots/click.wav')
shot = pygame.mixer.Sound('data/sound/oneshots/shot.wav')
newturn = pygame.mixer.Sound('data/sound/oneshots/newturn.wav')
