import pygame


class Lamp(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_up, sprite_down, sprite_right, sprite_left, id, group):
        super().__init__(group)
        self.id = id
        self.s_up = sprite_up
        self.s_down = sprite_down
        self.s_right = sprite_right
        self.s_left = sprite_left
        self.image = sprite_down
        self.rect = self.image.self.image.get_rect().move(x, y)

    def rotate_up(self):
        self.image = self.s_up
        self.rect = self.image.self.image.get_rect()

    def rotate_down(self):
        self.image = self.s_down
        self.rect = self.image.self.image.get_rect()

    def rotate_right(self):
        self.image = self.s_right
        self.rect = self.image.self.image.get_rect()

    def rotate_left(self):
        self.image = self.s_left
        self.rect = self.image.self.image.get_rect()

    def move(self, x, y):
        self.rect.move(x, y)