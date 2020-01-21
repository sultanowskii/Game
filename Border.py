import pygame


class Border(pygame.sprite.Sprite):
    def __init__(self, type, x1, y1, x2, y2, group):
        super().__init__(group)
        if type == "right":
            self.image = pygame.Surface([0, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 0, y2 - y1)
        elif type == "up":
            self.image = pygame.Surface([x2 - x1, 0])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 0)
        elif type == "left":
            self.image = pygame.Surface([0, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 0, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
