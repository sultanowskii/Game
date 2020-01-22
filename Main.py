import pygame
from Tile import Tile
from Enemy import Enemy
from Player import Player
from Border import Border
# from Button import Button
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
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pause_screen_cnecker = False
music_checker = True
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
music_off_button_sprite = load_image("music_off.png")
music_on_button_sprite = load_image("music_on.png")
# music_button = MusicButton(700, 20, music_on_button_sprite, music_off_button_sprite, buttons_group)

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
                new_player = Player(player_sprite, 0, 0,
                                    x * tile_width + (tile_width - charecter_width) / 2 + lx,
                                    y * tile_height + (tile_height - charecter_height) / 2 + ly, player_group)
            elif level[y][x] == '!':
                Tile('ground', x, y, grounds_group, all_sprites, tile_images, tile_width, tile_height, lx, ly)
                a = x * tile_width + (tile_width - charecter_width) // 2 + lx
                b = y * tile_height + (tile_height - charecter_height) // 2 + ly
                Enemy(enemy_sprite, 0, 0, a, b, enemies_group, level,
                      (a - lx) // tile_width, (b - ly) // tile_height)
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
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.pos == [0, 0]:  # buttons
        #         if music_buton.isMouseOn(event.pos):
        #             music_button.switch()
        #             if music_checker:
        #                 music_checker = False
        #                 pygame.mixer.stop()
        #             else:
        #                 music_checker = True
        #                 pygame.mixer.unpause()

    if going_down:
        #   if people can go and he wants go (key pressed), every iteration we move him to his speed
        player.move_down(1)
    if going_up:
        player.move_up(1)
    if going_right:
        player.move_right(1)
    if going_left:
        player.move_left(1)

    #   if people collided with wall, we make him go back (we must do this with player's speed)
    if pygame.sprite.spritecollideany(player, left_walls_group):
        player.move_left(1)
    if pygame.sprite.spritecollideany(player, right_walls_group):
        player.move_right(1)
    if pygame.sprite.spritecollideany(player, up_walls_group):
        player.move_up(1)
    if pygame.sprite.spritecollideany(player, down_walls_group):
        player.move_down(1)

    player_group.update()
    enemies_group.update()
    # buttons_group.update()
    right_walls_group.draw(screen)
    left_walls_group.draw(screen)
    up_walls_group.draw(screen)
    down_walls_group.draw(screen)
    grounds_group.draw(screen)
    enemies_group.draw(screen)
    player_group.draw(screen)
    walls_group.draw(screen)
    # buttons_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
