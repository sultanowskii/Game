import pygame


class MusicButton(pygame.sprite.Sprite):
    def __init__(self, x, y, on_sprite, off_sprite, group, size_x, size_y):
        super().__init__(group)
        self.on_sprite = on_sprite
        self.off_sprite = off_sprite
        self.image = on_sprite
        self.rect = self.image.get_rect().move(x, y)
        self.n = size_x
        self.m = size_y
        self.turned = True

    def isMouseOn(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.n:
            if self.rect.y <= pos[1] <= self.rect.y + self.m:
                return True
            else:
                return False
        else:
            return False

    def switch(self):
        if self.turned:
            self.turned = False
            self.image = self.off_sprite
        else:
            self.turned = True
            self.image = self.on_sprite