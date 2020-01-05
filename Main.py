import pygame
from AnimatedSprite import AnimatedSprite
from Camera import Camera
from Tile import Tile
import os

SIZE = X, Y = 800, 600
FPS = 60
BLACK = pygame.Color("black")

pygame.init()
screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
running = True
screen.fill(BLACK)
#   make a groups, additional functions


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


def start_screen(): #   Это висит как пример, потом переделай
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
                return
        pygame.display.flip()


def exit_game():    # quiting pygame
    running = False
    pygame.quit()


while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        #   all events checker
    pass
    #  here are updates of sprite groups
    pygame.display.flip()
    clock.tick(FPS)
