import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, size_x, size_y):
        super().__init__(group)
        self.n = size_x
        self.m = size_y
        self.x = x
        self.y = y

    def isMouseOn(self, pos):
        if self.x <= pos[0] <= self.x + self.n:
            if self.y <= pos[1] <= self.y + self.m:
                return True
            else:
                return False
        else:
            return False
