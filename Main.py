import pygame
from Camera import Camera
from Tile import Tile
from Enemy import Enemy
from Player import Player
from Border import Border
import os

SIZE = X, Y = 800, 600
FPS = 60
BLACK = pygame.Color("black")

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


screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
running = True
screen.fill(BLACK)
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
left_walls_group = pygame.sprite.Group()
right_walls_group = pygame.sprite.Group()
up_walls_group = pygame.sprite.Group()
down_walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
tile_width = tile_height = 50
player_sprite = load_image('player_sprite.png')
enemy_sprite = load_image('player_sprite.png')

def start_screen():  # Это висит как пример, потом переделай
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Ты умеешь ходить,",
                  "И все"]
    background = pygame.transform.scale(load_image('fon.jpg'), (X, Y))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany(player, walls, )
        pygame.display.flip()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, tiles_group, all_sprites, tile_images)
            elif level[y][x] == '#':
                Tile('wall', x, y, tiles_group, all_sprites, tile_images)
                Border("left", x * 50, y * 50, x * 50, (y + 1) * 50, left_walls_group)  # making invisible borders to checking collide
                Border("right", (x + 1) * 50, y * 50, (x + 1) * 50, (y + 1) * 50, right_walls_group) # I'm really not sure that it doesnt
                Border("up", x * 50, y * 50, (x + 1) * 50, y * 50, up_walls_group) # need have at least 1 width. If it does, just update
                Border("down", x * 50, (y + 1) * 50, (x + 1) * 50, (y + 1) * 50, down_walls_group) # it very early to make it covered with others titles and sprites.
            elif level[y][x] == '@':
                Tile('empty', x, y, tiles_group, all_sprites, tile_images)
                new_player = Player(player_sprite, ENTER_HERE_COLUMNS_AND_ROWS, x * 50, y * 50, player_group)
            elif level[y][x] == '!':
                Enemy(enemy_sprite, ENTER_HERE_COLUMNS_AND_ROWS, x * 50, y * 50, enemies_group)
    return new_player, x, y


def exit_game():  # quiting pygame
    running = False
    pygame.quit()


while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not pygame.sprite.spritecollideany(player, right_walls_group): # checking if our player collide with some wall from any side
                player.move_right()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not pygame.sprite.spritecollideany(player, left_walls_group):
                player.move_left()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if not pygame.sprite.spritecollideany(player, up_walls_group):
                player.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if not pygame.sprite.spritecollideany(player, down_walls_group):
                player.move_down()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos: # buttons
                pass
    #  here are updates of sprite groups
    # dont forget about Camera
    pygame.display.flip()
    clock.tick(FPS)
