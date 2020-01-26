import pygame
import os


#   игрок
class Player(pygame.sprite.Sprite):
    def __init__(self, staying, sheet_up, sheet_down, sheet_right, sheet_left, columns, rows, x, y, group):
        super().__init__(group)
        self.curr_looking = "staying"
        self.stay = staying
        self.s_up = sheet_up
        self.s_down = sheet_down
        self.s_right = sheet_right
        self.s_left = sheet_left
        self.columns = columns
        self.rows = rows
        self.image = self.stay
        self.rect = self.image.get_rect().move(x, y)
        self.cntr = 0
        self.frames = []

    #   функции смены анимаций спрайта в зависимости от направления движения
    def stay_on(self):
        self.curr_looking = "staying"
        self.image = self.stay
        self.cntr = 0
        self.frames = []

    def move_up(self, speed):
        self.rect.y -= speed
        if self.curr_looking != "up":
            self.curr_looking = "up"
            self.frames = []
            self.cut_sheet(self.s_up, self.columns, self.rows)
            self.cntr = 0

    def move_down(self, speed):
        self.rect.y += speed
        if self.curr_looking != "down":
            self.curr_looking = "down"
            self.frames = []
            self.cut_sheet(self.s_down, self.columns, self.rows)
            self.cntr = 0

    def move_right(self, speed):
        self.rect.x += speed
        if self.curr_looking != "right":
            self.curr_looking = "right"
            self.frames = []
            self.cut_sheet(self.s_right, self.columns, self.rows)
            self.cntr = 0

    def move_left(self, speed):
        self.rect.x -= speed
        if self.curr_looking != "left":
            self.curr_looking = "left"
            self.frames = []
            self.cut_sheet(self.s_left, self.columns, self.rows)
            self.cntr = 0

    #   разрезание изображения на кадры
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.curr_looking == "staying":
            self.image = self.stay
        else:
            if (self.cntr + 1) % 5 == 0:
                self.image = self.frames[self.cntr // 5]
        self.cntr = (self.cntr + 1) % 20
        #   увеличиваем время смены спрайтов в 5 раз, умножая кол-во кадров в 5 раз и деля их в индексе
