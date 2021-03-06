import pygame


#   тайл, в нашей игре их 2 вида - стена и пол
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, group, tile_list, tile_width, tile_height, lx, ly):
        super().__init__(group)
        self.image = tile_list[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + lx, tile_height * pos_y + ly)