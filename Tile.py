import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, group, main_group, tile_list, tile_width, tile_height):
        super().__init__(group, main_group)
        self.image = tile_list[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
