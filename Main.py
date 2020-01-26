import pygame
import os
import sys

from Tile import Tile
from Enemy import Enemy
from Player import Player
from Border import Border
from MusicButton import MusicButton
from Lamp import Lamp
from PauseButton import PauseButton

SIZE = X, Y = 800, 600
FPS = 60
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")

pygame.init()


def load_image(name, colorkey=None):    #   загрузка изображения и создание прозрачного фона
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


screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
screen.fill(BLACK)

tile_width = tile_height = 48
charecter_height = charecter_width = 24
lx = -1 # отступы поля от границы экрана
ly = -1

going_up = False
going_down = False
going_right = False
going_left = False
running = True

lamp_up_sprite = load_image("lamp_up.png", (235, 255, 255))
lamp_down_sprite = load_image("lamp_down.png", (235, 255, 255))
lamp_right_sprite = load_image("lamp_right.png", (235, 255, 255))
lamp_left_sprite = load_image("lamp_left.png", (235, 255, 255))
tile_images = {'wall': load_image('wall.png'), 'ground': load_image('ground.png')}
player_sprite = load_image('player_sprite.png', (236, 255, 255))
enemy_sprite = load_image('enemy_sprite.png', (236, 255, 255))

music_off_button_sprite = load_image("music_off.png")
music_on_button_sprite = load_image("music_on.png")
pause_button_sprite = load_image("pause_button.png")

pl_down_sprite = load_image("player_sprite_down.png", -1)
pl_up_sprite = load_image("player_sprite_up.png", -1)
pl_right_sprite = load_image("player_sprite_right.png", -1)
pl_left_sprite = load_image("player_sprite_left.png", -1)
en_down_sprite = load_image("enemy_sprite_down.png", -1)
en_up_sprite = load_image("enemy_sprite_up.png", -1)
en_right_sprite = load_image("enemy_sprite_right.png", -1)
en_left_sprite = load_image("enemy_sprite_left.png", -1)

main_music = 'data/music.mp3'  # Jason Garner & Vince de Vera – Creepy Forest (Vinyl) (Don t Starve OST)
sound_of_death = pygame.mixer.Sound('data/sound_of_death.ogg')

lamps_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
grounds_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

left_walls_group = pygame.sprite.Group()
right_walls_group = pygame.sprite.Group()
up_walls_group = pygame.sprite.Group()
down_walls_group = pygame.sprite.Group()
right_up_corner_group = pygame.sprite.Group()
left_up_corner_group = pygame.sprite.Group()
right_down_corner_group = pygame.sprite.Group()
left_down_corner_group = pygame.sprite.Group()


music_button = MusicButton(695, 5, music_on_button_sprite, music_off_button_sprite, buttons_group, 100, 44)
pause_button = PauseButton(645, 5, pause_button_sprite, buttons_group, 44, 44)
player = None


def start_screen():
    x = 1
    y = 1
    print("\033[33mПривет! Нажав в игровом окне любую кнопку, вы загрузите уровни,")
    print("созданные \033[35mразработичками.\033[0m")
    print("\033[33mЕсли же вы хотите сыграть в \033[32mсвой уровень\033[33m (инструкция по ее созданию")
    print("\033[33mесть в папке с игрой), то тогда нажмите с открытым окном клавишу '"
          "'5'',\nпотом вставьте сюда название своего уровня, ", end="")
    print("если хотите сыграть на своем (не забудьте дописать ''.txt''):\n")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_5: #   если нажата кнопкаа "5", то ждем от юзера названия уровня
                    level = input()
                    return level
                return
        background = pygame.transform.scale(load_image(f'bck_frames\\bck_start{x}.png'), (X, Y))
        text = pygame.transform.scale(load_image(f'continue_text\\press_text{y // 5 + 1}.png', (235, 255, 255)), (810, 54))
        screen.blit(background, (0, 0))
        screen.blit(text, (-3, 530))
        x = (x + 1) % 40 + 1
        y = (y + 1) % 40 + 1
        pygame.display.flip()
        clock.tick(FPS)


def next_level_screen():
    x = 1
    y = 1
    print("Нажмите ''5'' и введите название уровня, "
          "если хотите запустить свой уровень, в другом случае нажмите любую кнопку")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_5: #   если нажата кнопкаа "5", то ждем от юзера названия уровня
                    level = input()
                    return level
                return
        background = pygame.transform.scale(load_image(f'bck_frames\\bck_start{x}.png'), (X, Y))
        text = pygame.transform.scale(load_image(f'continue_text\\press_text{y // 5 + 1}.png', (235, 255, 255)), (810, 54))
        screen.blit(background, (0, 0))
        screen.blit(text, (-3, 530))
        x = (x + 1) % 40 + 1
        y = (y + 1) % 40 + 1
        pygame.display.flip()
        clock.tick(FPS)

def pause_screen():
    x = 1
    y = 1
    pause_table = pygame.transform.scale(load_image("pause_text.png", (235, 255, 255)), (720, 171))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                return
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        background = pygame.transform.scale(load_image(f'bck_frames\\bck_start{x}.png'), (X, Y))
        text = pygame.transform.scale(load_image(f'continue_text\\press_text{y // 5 + 1}.png', (235, 255, 255)),
                                      (810, 54))
        screen.blit(background, (0, 0))
        screen.blit(text, (-3, 530))
        screen.blit(pause_table, (45, 5))
        x = (x + 1) % 40 + 1
        y = (y + 1) % 40 + 1    # увеличиваем время между сменой кадров (умножаем на 5, и в строке
        #   присваивания (text = ...) делим его на 5)
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
    ens = 0
    id_cntr = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('ground', x, y, grounds_group, tile_images, tile_width, tile_height, lx, ly)
            elif level[y][x] == '#':
                Tile('wall', x, y, walls_group, tile_images, tile_width, tile_height, lx, ly)
                # для каждой стены создаем невидимые барьеры
                Border("left", x * tile_width + lx, y * tile_height + ly + 1, x * tile_width + lx,
                       (y + 1) * tile_height + ly - 1,
                       left_walls_group)
                Border("right", (x + 1) * tile_width + lx - 1, y * tile_height + ly + 1, (x + 1) * tile_width + lx - 1,
                       (y + 1) * tile_height + ly - 1,
                       right_walls_group)
                Border("up", x * tile_width + lx + 1, y * tile_height + ly, (x + 1) * tile_width + lx - 1,
                       y * tile_height + ly,
                       up_walls_group)
                Border("down", x * tile_width + lx + 1, (y + 1) * tile_height + ly - 1, (x + 1) * tile_width + lx - 1,
                       (y + 1) * tile_height + ly - 1,
                       down_walls_group)
                Border("corner", x * tile_width + lx, y * tile_height + ly, x * tile_width + lx, y * tile_height + ly,
                       left_up_corner_group)
                Border("corner", (x + 1) * tile_width + lx - 1, y * tile_height + ly, (x + 1) * tile_width + lx - 1, y * tile_height + ly,
                       right_up_corner_group)
                Border("corner", x * tile_width + lx, (y + 1) * tile_height + ly - 1, x * tile_width + lx, (y + 1) * tile_height + ly - 1,
                       left_down_corner_group)
                Border("corner", (x + 1) * tile_width + lx - 1, (y + 1) * tile_height + ly - 1, (x + 1) * tile_width + lx - 1, (y + 1) * tile_height + ly - 1,
                       right_down_corner_group)
            elif level[y][x] == '@':
                Tile('ground', x, y, grounds_group, tile_images, tile_width, tile_height, lx, ly)
                player_group.empty()
                new_player = Player(player_sprite, pl_up_sprite, pl_down_sprite, pl_right_sprite, pl_left_sprite, 4, 1,
                                    x * tile_width + (tile_width - charecter_width) / 2 + lx,
                                    y * tile_height + (tile_height - charecter_height) / 2 + ly, player_group)
            elif level[y][x] == '!':
                Tile('ground', x, y, grounds_group, tile_images, tile_width, tile_height, lx, ly)
                a = x * tile_width + (tile_width - charecter_width) // 2 + lx
                b = y * tile_height + (tile_height - charecter_height) // 2 + ly
                ens += 1
                curr_enemy = Enemy(enemy_sprite, en_up_sprite, en_down_sprite, en_right_sprite, en_left_sprite, 4, 1, a, b, enemies_group, level,
                      (a - lx) // tile_width, (b - ly) // tile_height, id_cntr)
                curr_lamp = Lamp(curr_enemy.rect.x, curr_enemy.rect.y, lamp_up_sprite, lamp_down_sprite, lamp_right_sprite, lamp_left_sprite, id_cntr, lamps_group)
                curr_enemy.lamp = curr_lamp
                id_cntr += 1
    #  создание невидимых границ уровня, чтобы игрок не смог выйти за его пределы:
    Border("right", lx, ly, lx, (y + 1) * tile_height + ly, right_walls_group)
    Border("left", lx + (x + 1) * tile_width, ly, lx + (x + 1) * tile_width, (y + 1) * tile_height + ly, left_walls_group)
    Border("down", lx, ly, lx + (x + 1) * tile_width, ly, down_walls_group)
    Border("up", lx, ly + (y + 1) * tile_height, lx + (x + 1) * tile_width, (y + 1) * tile_height + ly, up_walls_group)
    return new_player, x, y, level, ens


def terminate():
    pygame.quit()
    print("\033[36mСпасибо, что играли в нашу игру!")
    sys.exit()


pygame.mixer.music.load(main_music)
pygame.mixer.music.play(1000000)
#   ну что бы наверняка


def clear_groups(): #   очистка
    lamps_group.empty()
    grounds_group.empty()
    walls_group.empty()
    left_walls_group.empty()
    right_walls_group.empty()
    up_walls_group.empty()
    down_walls_group.empty()
    player_group.empty()
    enemies_group.empty()


def main(al_cntr):  #   основной игровой цикл
    going_up = False
    going_down = False
    going_right = False
    going_left = False
    alive_cntr = al_cntr
    while running and alive_cntr > 0:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                break
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
                    # Перестаем бегать, если кнопка отжата
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
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    music_button.switch()
                if pause_button.isMouseOn(event.pos):
                    pause_screen()
                    break
        went_anywhere = False
        if going_down:
            #   если игрок может пойти куда-то (проверятся в цикле обработки событий) и
            #   он хочет туда пойти (кнопка зажата), то тогда каждую итерацию перемещаем его на его скорость
            went_anywhere = True
            player.move_down(2)
            if pygame.sprite.spritecollideany(player, up_walls_group):
                player.move_up(2)
        if going_up:
            player.move_up(2)
            went_anywhere = True
            if pygame.sprite.spritecollideany(player, down_walls_group):
                player.move_down(2)
        if going_right:
            player.move_right(2)
            went_anywhere = True
            if pygame.sprite.spritecollideany(player, left_walls_group):
                player.move_left(2)
        if going_left:
            player.move_left(2)
            went_anywhere = True
            if pygame.sprite.spritecollideany(player, right_walls_group):
                player.move_right(2)
        if not went_anywhere:
            player.stay_on()

        #   вручную пробегаемся по всем противникам,
        #   и если мы сопприкасаемся в с кем-то, то убиваем его
        for enemy in enemies_group:
            if pygame.sprite.collide_rect(player, enemy) and not enemy.dead:
                sound_of_death.play()
                alive_cntr -= 1
                enemy.kill()

        if pygame.sprite.spritecollideany(player, lamps_group):
            sound_of_death.play()
            return True

        player_group.update()
        enemies_group.update()
        buttons_group.update()
        grounds_group.draw(screen)
        lamps_group.draw(screen)
        enemies_group.draw(screen)
        player_group.draw(screen)
        walls_group.draw(screen)
        buttons_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


curr_level = start_screen()
#   проверка на то, ввел ли пользователь название карты или решил сыграть в готовые уровни
if curr_level != None:
    try:
        while curr_level != None:
            isPlayerDead = True
            while isPlayerDead:
                player, level_x, level_y, level_map, enemies_cntr = generate_level(load_level(f"levels/{curr_level}"))
                running = True
                isPlayerDead = main(enemies_cntr)
                clear_groups()
            next_level_screen()
    except FileNotFoundError:
        print("\033[31mОшибка 101: Файл не найден")
else:
    try:
        for i in range(1, 21):
            isPlayerDead = True
            while isPlayerDead:
                player, level_x, level_y, level_map, enemies_cntr = generate_level(load_level(f"levels/level{i}.txt"))
                running = True
                isPlayerDead = main(enemies_cntr)
                clear_groups()
            next_level_screen()
    except FileNotFoundError:
        print("\033[31mОшибка 102: Системный файл карты уровня не найден")
terminate()
