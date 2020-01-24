import pygame


#   лампа полицейских, служит для обнаружения игрока
class Lamp(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_up, sprite_down, sprite_right, sprite_left, id, group):
        super().__init__(group)
        self.id = id
        self.s_up = sprite_up
        self.s_down = sprite_down
        self.s_right = sprite_right
        self.s_left = sprite_left
        self.image = sprite_down
        self.rect = self.image.get_rect().move(x, y)

    #   функции поворота и праильного перемещения лампы относительно ее владельца
    def rotate_up(self, x, y):
        self.image = self.s_up
        self.rect = self.image.get_rect()
        self.rect.x = x - 12
        self.rect.y = y - 60

    def rotate_down(self, x, y):
        self.image = self.s_down
        self.rect = self.image.get_rect()
        self.rect.x = x - 12
        self.rect.y = y + 25

    def rotate_right(self, x, y):
        self.image = self.s_right
        self.rect = self.image.get_rect()
        self.rect.x = x + 25
        self.rect.y = y - 13

    def rotate_left(self, x, y):
        self.image = self.s_left
        self.rect = self.image.get_rect()
        self.rect.x = x - 60
        self.rect.y = y - 12