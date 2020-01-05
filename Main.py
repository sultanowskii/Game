import pygame
from AnimatedSprite import AnimatedSprite
from Camera import Camera
from Tile import Tile


SIZE = X, Y = 800, 600
FPS = 60
BLACK = pygame.Color("black")

pygame.init()
screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
running = True
screen.fill(BLACK)
#   make a groups, additional functions


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
