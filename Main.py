import pygame
from Tile import Tile
from Enemy import Enemy
from Player import Player
from Border import Border
from MusicButton import MusicButton
from Lamp import Lamp
import os
import sys

SIZE = X, Y = 800, 600
FPS = 60
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image = image.convert()
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pause_screen_cnecker = False
running = True

main_music = 'data/music.mp3'  # Jason Garner & Vince de Vera – Creepy Forest (Vinyl) (Don t Starve OST)

screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
screen.fill(BLACK)
tile_width = tile_height = 48
charecter_height = charecter_width = 24
player = None
lx = -1
ly = -1
ground_width = 0
ground_height = 0
going_up = False
going_down = False
going_right = False
going_left = False
lamp_up_sprite = load_image("lamp_up.png", (235, 255, 255))
lamp_down_sprite = load_image("lamp_down.png", (235, 255, 255))
lamp_right_sprite = load_image("lamp_right.png", (235, 255, 255))
lamp_left_sprite = load_image("lamp_left.png", (235, 255, 255))
music_off_button_sprite = load_image("music_off.png")
music_on_button_sprite = load_image("music_on.png")
pl_down_sprite = load_image("player_sprite_down.png", -1)
pl_up_sprite = load_image("player_sprite_up.png", -1)
pl_right_sprite = load_image("player_sprite_right.png", -1)
pl_left_sprite = load_image("player_sprite_left.png", -1)
en_down_sprite = load_image("enemy_sprite_down.png", -1)
en_up_sprite = load_image("enemy_sprite_up.png", -1)
en_right_sprite = load_image("enemy_sprite_right.png", -1)
en_left_sprite = load_image("enemy_sprite_left.png", -1)

lamps_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
grounds_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
left_walls_group = pygame.sprite.Group()
right_walls_group = pygame.sprite.Group()
up_walls_group = pygame.sprite.Group()
down_walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

tile_images = {'wall': load_image('wall.png'), 'ground': load_image('ground.png')}
player_sprite = load_image('player_sprite.png', (236, 255, 255))
enemy_sprite = load_image('enemy_sprite.png', (236, 255, 255))

music_button = MusicButton(680, 20, music_on_button_sprite, music_off_button_sprite, buttons_group, 100, 44)


def start_screen():
    x = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                return
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        background = pygame.transform.scale(load_image(f'bck_frames\\bck_start{x % 40 + 1}.png'), (X, Y))
        screen.blit(background, (0, 0))
        x += 1
        pygame.display.flip()
        clock.tick(FPS)


def pause_screen():
    background = pygame.transform.scale(load_image('background_pause.jpg'), (X, Y))
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    ly = (Y - len(level) * tile_height) // 2
    lx = (X - len(level[0]) * tile_width) // 2
    ground_height = len(level)
    ground_width = len(level[0])
    id_cntr = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('ground', x, y, grounds_group, all_sprites, tile_images, tile_width, tile_height, lx, ly)
            elif level[y][x] == '#':
                Tile('wall', x, y, walls_group, all_sprites, tile_images, tile_width, tile_height, lx, ly)
                Border("left", x * tile_width + lx, y * tile_height + ly + 1, x * tile_width + lx,
                       (y + 1) * tile_height + ly - 2,
                       left_walls_group)  # making invisible borders to checking collide
                Border("right", (x + 1) * tile_width + lx, y * tile_height + ly + 1, (x + 1) * tile_width + lx,
                       (y + 1) * tile_height + ly - 2,
                       right_walls_group)  # I'm really not sure that it doesnt
                Border("up", x * tile_width + lx + 1, y * tile_height + ly, (x + 1) * tile_width + lx - 2,
                       y * tile_height + ly,
                       up_walls_group)  # need have at least 1 width. If it does, just update
                Border("down", x * tile_width + lx + 1, (y + 1) * tile_height + ly - 1, (x + 1) * tile_width + lx - 2,
                       (y + 1) * tile_height + ly - 1,
                       down_walls_group)  # it very early to make it covered with others titles and sprites.
            elif level[y][x] == '@':
                Tile('ground', x, y, grounds_group, all_sprites, tile_images, tile_width, tile_height, lx, ly)
                new_player = Player(player_sprite, pl_up_sprite, pl_down_sprite, pl_right_sprite, pl_left_sprite, 4, 1,
                                    x * tile_width + (tile_width - charecter_width) / 2 + lx,
                                    y * tile_height + (tile_height - charecter_height) / 2 + ly, player_group)
            elif level[y][x] == '!':
                Tile('ground', x, y, grounds_group, all_sprites, tile_images, tile_width, tile_height, lx, ly)
                a = x * tile_width + (tile_width - charecter_width) // 2 + lx
                b = y * tile_height + (tile_height - charecter_height) // 2 + ly
                curr_enemy = Enemy(enemy_sprite, en_up_sprite, en_down_sprite, en_right_sprite, en_left_sprite, 4, 1, a, b, enemies_group, level,
                      (a - lx) // tile_width, (b - ly) // tile_height, id_cntr)
                curr_lamp = Lamp(curr_enemy.rect.x, curr_enemy.rect.y, lamp_up_sprite, lamp_down_sprite, lamp_right_sprite, lamp_left_sprite, id_cntr, lamps_group)
                curr_enemy.lamp = curr_lamp
                id_cntr += 1
    Border("right", lx, ly, lx, (y + 1) * tile_height + ly, right_walls_group)
    Border("left", lx + (x + 1) * tile_width, ly, lx + (x + 1) * tile_width, (y + 1) * tile_height + ly, left_walls_group)
    Border("down", lx, ly, lx + (x + 1) * tile_width, ly, down_walls_group)
    Border("up", lx, ly + (y + 1) * tile_height, lx + (x + 1) * tile_width, (y + 1) * tile_height + ly, up_walls_group)
    return new_player, x, y, level


def terminate():
    pygame.quit()
    sys.exit()


pygame.mixer.music.load(main_music)
pygame.mixer.music.play(1000000)
player, level_x, level_y, level_map = generate_level(load_level("level.txt"))
start_screen()
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
            break
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_screen()
                break
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if not pygame.sprite.spritecollideany(player,
                                                      left_walls_group):
                    # checking if our player collide with some wall from any side
                    going_right = True
                else:
                    going_right = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if not pygame.sprite.spritecollideany(player, right_walls_group):
                    going_left = True
                else:
                    going_left = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if not pygame.sprite.spritecollideany(player, down_walls_group):
                    going_up = True
                else:
                    going_up = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if not pygame.sprite.spritecollideany(player, up_walls_group):
                    going_down = True
                else:
                    going_down = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # Turning off moving if we stopped pressing key
                going_right = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                going_left = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                going_up = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                going_down = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if music_button.isMouseOn(event.pos):
                if music_button.turned:
                    print("hey")
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                music_button.switch()

    went_anywhere = False
    if going_down:
        #   if people can go and he wants go (key pressed), every iteration we move him to his speed
        went_anywhere = True
        player.move_down(2)
    if going_up:
        player.move_up(2)
        went_anywhere = True
    if going_right:
        player.move_right(2)
        went_anywhere = True
    if going_left:
        player.move_left(2)
        went_anywhere = True
    if not went_anywhere:
        player.stay_on()

    #   if people collided with wall, we make him go back (we must do this with player's speed)
    if pygame.sprite.spritecollideany(player, left_walls_group):
        player.move_left(2)
    if pygame.sprite.spritecollideany(player, right_walls_group):
        player.move_right(2)
    if pygame.sprite.spritecollideany(player, up_walls_group):
        player.move_up(2)
    if pygame.sprite.spritecollideany(player, down_walls_group):
        player.move_down(2)

    for enemy in enemies_group:
        if pygame.sprite.collide_rect(player, enemy):
            enemy.kill()

    player_group.update()
    enemies_group.update()
    buttons_group.update()
    right_walls_group.draw(screen)
    left_walls_group.draw(screen)
    up_walls_group.draw(screen)
    down_walls_group.draw(screen)
    grounds_group.draw(screen)
    lamps_group.draw(screen)
    enemies_group.draw(screen)
    player_group.draw(screen)
    walls_group.draw(screen)
    buttons_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
