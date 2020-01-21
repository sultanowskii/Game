import pygame
from AnimatedSprite import AnimatedSprite
import random


class Enemy(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, group, map, y_map_now, x_map_now):  # think about making a mask here
        super().__init__(sheet, columns, rows, x, y, group)
        self.n = 4
        self.m = 4
        self.x_go_now = 0
        self.y_go_now = 0
        self.absolute_x = x
        self.absolute_y = y
        self.map = map  # карта n * m, где "." - свободное место, а "#" - стена
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

    def kill(self):
        self.rect.move(10000, 10000)
        self.dead = True
        self.way_y = []
        self.way_x = []
        self.way_x, self.way_y = self.group.make_way(self.x_now, self.y_now)

    def cut_sheet(self, sheet, columns, rows):
        super().cut_sheet(sheet, columns, rows)

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
            used = [[False] * self.n] * self.m
            way_x = [[0] * self.n] * self.m
            way_y = [[0] * self.n] * self.m
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
            way_for_x.append(x)
            way_for_y.append(y)
            if x - 1 >= 0 and (way_y[x - 1][y] != 0 or way_x[x - 1][y] != 0):
                x -= 1
            elif x + 1 < self.n and (way_y[x + 1][y] != 0 or way_x[x + 1][y] != 0):
                x += 1
            elif y - 1 >= 0 and (way_x[x][y - 1] != 0 or way_y[x][y - 1] != 0):
                y -= 1
            elif y + 1 < self.m and (way_x[x][y + 1] != 0 or way_y[x][y + 1] != 0):
                y += 1
            # на данном этапе x и y это координаты, откуда мы пришли в точку (x_where, y_where)
            while x != x_player or y != y_player:  # идём по предкам и находим путь
                way_for_x.append(x)
                way_for_y.append(y)
                c = x
                x = way_x[x][y]
                y = way_x[c][y]
            way_for_y.append(y)
            way_for_x.append(x)
            return way_for_x, way_for_y

    def where_to_now(self, x_now, y_now):
        if not self.dead:
            x_now = int(x_now)
            y_now = int(y_now)

            b = random.randint(0, 3)
            a = [False] * 4
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
                    else:
                        self.rect.y += 1
                else:
                    if self.y_now > self.y_go_now:
                        self.rect.x -= 1
                    else:
                        self.rect.x += 1
            else:
                self.step_cntr = 0
                self.last_x = self.x_now
                self.last_y = self.y_now
                self.x_now = self.x_go_now
                self.y_now = self.y_go_now
