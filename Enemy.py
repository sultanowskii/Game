import pygame
from AnimatedSprite import AnimatedSprite
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, staying, sheet_up, sheet_down, sheet_right, sheet_left, columns, rows, x, y, group, map, y_map_now, x_map_now,
                 id):  # think about making a mask here
        super().__init__(group)
        self.lamp = None
        self.id = id
        self.image = staying
        self.rect = self.image.get_rect().move(x, y)
        self.x_go_now = -1
        self.y_go_now = -1
        self.absolute_x = x
        self.absolute_y = y
        self.map = map  # карта n * m, где "." - свободное место, а "#" - стена
        self.n = len(map)
        self.m = len(map[0])
        self.dead = False
        self.step_cntr = 0
        self.x_now = x_map_now  # х сейчас
        self.y_now = y_map_now  # у сейчас
        self.x_now = int(self.x_now)
        self.y_now = int(self.y_now)
        if self.can_go_right(self.x_now, self.y_now):
            self.last_x = self.x_now
            self.last_y = self.y_now + 1
        elif self.can_go_left(self.x_now, self.y_now):
            self.last_x = self.x_now
            self.last_y = self.y_now - 1
        elif self.can_go_up(self.x_now, self.y_now):
            self.last_x = self.x_now - 1
            self.last_y = self.y_now
        elif self.can_go_down(self.x_now, self.y_now):
            self.last_x = self.x_now + 1
            self.last_y = self.y_now
        self.group = group
        self.way_x = []
        self.way_y = []

        self.frames = []
        self.stay = staying
        self.s_up = sheet_up
        self.s_down = sheet_down
        self.s_right = sheet_right
        self.s_left = sheet_left
        self.columns = columns
        self.rows = rows
        self.cntr = 0
        self.curr_looking = "staying"

    def kill(self):
        if not self.dead:
            self.dead = True
            self.way_y = []
            self.way_x = []
            for en in self.group:
                if en.id != self.id:
                    if self.y_go_now != -1 and self.x_go_now != -1:
                        en.make_way(self.x_go_now, self.y_go_now)
                    else:
                        en.make_way(self.x_now, self.y_now)
            for i in range(len(self.way_x)):
                print(self.way_x[i], self.way_y[i])
            print()
            self.rect.x = -100
            self.rect.y = -100
            self.lamp.rect.x = -100
            self.lamp.rect.y = -100

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def can_go_right(self, x, y):
        if y + 1 < self.m and self.map[x][y + 1] != "#":
            return True
        else:
            return False

    def can_go_left(self, x, y):
        if y - 1 >= 0 and self.map[x][y - 1] != "#":
            return True
        else:
            return False

    def can_go_down(self, x, y):
        if x + 1 < self.n and self.map[x + 1][y] != "#":
            return True
        else:
            return False

    def can_go_up(self, x, y):
        if x - 1 >= 0 and self.map[x - 1][y] != "#":
            return True
        else:
            return False

    def make_way(self, x_where, y_where):
        if not self.dead:
            x_player = self.x_now
            y_player = self.y_now
            used = []
            for i in range(self.n):
                help = []
                for j in range(self.m):
                    help.append(False)
                used.append(help)
            way_x = []
            way_y = []
            for i in range(self.n):
                help = []
                for j in range(self.m):
                    help.append(0)
                way_y.append(help)
            for i in range(self.n):
                help = []
                for j in range(self.m):
                    help.append(0)
                way_x.append(help)
            dfs_x = []
            dfs_y = []
            dfs_x.append(x_player)
            dfs_y.append(y_player)
            while len(dfs_y) != 0:  # кратчайший путь от точки (x_player, y_player) до точки (x_where, y_where)
                x = dfs_x[0]
                y = dfs_y[0]
                del (dfs_x[0])
                del [dfs_y[0]]
                used[x][y] = True
                if self.can_go_up(x, y) and not (used[x - 1][y]):
                    dfs_x.append(x - 1)
                    dfs_y.append(y)
                    way_x[x - 1][y] = x
                    way_y[x - 1][y] = y
                if self.can_go_down(x, y) and not (used[x + 1][y]):
                    dfs_x.append(x + 1)
                    dfs_y.append(y)
                    way_x[x + 1][y] = x
                    way_y[x + 1][y] = y
                if self.can_go_left(x, y) and not (used[x][y - 1]):
                    dfs_x.append(x)
                    dfs_y.append(y - 1)
                    way_x[x][y - 1] = x
                    way_y[x][y - 1] = y
                if self.can_go_right(x, y) and not (used[x][y + 1]):
                    dfs_x.append(x)
                    dfs_y.append(y + 1)
                    way_x[x][y + 1] = x
                    way_y[x][y + 1] = y
                if x == x_where and y == y_where:
                    break
            x = x_where
            y = y_where
            way_for_x = []
            way_for_y = []
            if x - 1 >= 0 and (way_y[x - 1][y] != 0 or way_x[x - 1][y] != 0):
                x -= 1
            elif x + 1 < self.n and (way_y[x + 1][y] != 0 or way_x[x + 1][y] != 0):
                x += 1
            elif y - 1 >= 0 and (way_x[x][y - 1] != 0 or way_y[x][y - 1] != 0):
                y -= 1
            elif y + 1 < self.m and (way_x[x][y + 1] != 0 or way_y[x][y + 1] != 0):
                y += 1
            while x != x_player or y != y_player:  # идём по предкам и находим путь
                way_for_x.append(x)
                way_for_y.append(y)
                c = x
                x = way_x[x][y]
                y = way_y[c][y]
            way_for_y.append(y)
            way_for_x.append(x)
            way_for_x.reverse()
            way_for_y.reverse()
            self.way_x = way_for_x
            self.way_y = way_for_y

    def where_to_now(self, x_now, y_now):
        if not self.dead:
            x_now = int(x_now)
            y_now = int(y_now)
            b = random.randint(0, 3)
            a = []
            for i in range(4):
                a.append(False)
            if self.can_go_left(x_now, y_now):
                a[0] = True
            if self.can_go_right(x_now, y_now):
                a[1] = True
            if self.can_go_up(x_now, y_now):
                a[2] = True
            if self.can_go_down(x_now, y_now):
                a[3] = True
            while not a[b]:
                b = random.randint(0, 3)
            if b == 0:
                return x_now, y_now - 1
            if b == 1:
                return x_now, y_now + 1
            if b == 2:
                return x_now - 1, y_now
            return x_now + 1, y_now

    def update(self):
        if not self.dead:
            if self.step_cntr == 0:
                if len(self.way_x) == 0:
                    self.x_go_now, self.y_go_now = self.where_to_now(self.x_now, self.y_now)
                else:
                    self.x_go_now = self.way_x[0]
                    self.y_go_now = self.way_y[0]
                    del (self.way_x[0])
                    del (self.way_y[0])
            if 0 <= self.step_cntr < 49:
                self.step_cntr += 1
                if self.x_now != self.x_go_now:
                    if self.x_now > self.x_go_now:
                        self.rect.y -= 1
                        self.lamp.rotate_up(self.rect.x, self.rect.y)
                        if self.curr_looking != "up":
                            self.curr_looking = "up"
                            self.frames = []
                            self.cut_sheet(self.s_up, self.columns, self.rows)
                            self.cntr = 0
                    else:
                        self.rect.y += 1
                        self.lamp.rotate_down(self.rect.x, self.rect.y)
                        if self.curr_looking != "down":
                            self.curr_looking = "down"
                            self.frames = []
                            self.cut_sheet(self.s_down, self.columns, self.rows)
                            self.cntr = 0
                else:
                    if self.y_now > self.y_go_now:
                        self.rect.x -= 1
                        self.lamp.rotate_left(self.rect.x, self.rect.y)
                        if self.curr_looking != "left":
                            self.curr_looking = "left"
                            self.frames = []
                            self.cut_sheet(self.s_left, self.columns, self.rows)
                            self.cntr = 0
                    else:
                        self.rect.x += 1
                        self.lamp.rotate_right(self.rect.x, self.rect.y)
                        if self.curr_looking != "right":
                            self.curr_looking = "right"
                            self.frames = []
                            self.cut_sheet(self.s_right, self.columns, self.rows)
                            self.cntr = 0
            else:
                self.step_cntr = 0
                self.last_x = self.x_now
                self.last_y = self.y_now
                self.x_now = self.x_go_now
                self.y_now = self.y_go_now
            if (self.cntr + 1) % 5 == 0:
                self.image = self.frames[self.cntr // 5]
            self.cntr = (self.cntr + 1) % 20