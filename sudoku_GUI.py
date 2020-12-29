import sys
import copy
import pygame as pg
import sudoku

pg.init()
win = pg.display.set_mode((450, 500))
pg.display.set_caption('Sudoku Solver')
enterFont = pg.font.Font('SourceSansPro-Regular.ttf', 30)

class Box():
    def __init__(self, rect, value, pos):
        self.rect = pg.Rect(rect)
        self.value = value
        self.pencil = 0
        self.highlighted = False
        self.visited = False
        self.correct = False
        self.wrong = False
        self.pos = pos

    def draw(self):
        if self.highlighted:
            pg.draw.rect(win, (187, 222, 251), (self.rect.x + 1, self.rect.y + 1, 49, 49))
        if self.correct:
            pg.draw.rect(win, (0, 255, 0), (self.rect.x + 1, self.rect.y + 1, 48, 48), 2)
        elif self.wrong:
            pg.draw.rect(win, (255, 0, 0), (self.rect.x + 1, self.rect.y + 1, 48, 48), 2)
        if self.value != 0 or self.wrong:
            number_surface = enterFont.render(str(self.value), True, (0, 0, 0))
            number_rect = number_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            win.blit(number_surface, number_rect)

class Grid():
    def __init__(self, grid):
        self.grid = grid
        self.player_grid = copy.deepcopy(grid)
        self.formatted = self.format()

    def draw(self):
        for i in range(10):
            if i % 3 == 0:
                pg.draw.rect(win, (0, 0, 0), (i * 50 - 1.5, 0, 3, 450))
                pg.draw.rect(win, (0, 0, 0), (0, i * 50 - 1.5, 450, 3))
            else:
                pg.draw.rect(win, (0, 0, 0), (i * 50, 0, 1, 450))
                pg.draw.rect(win, (0, 0, 0), (0, i * 50, 450, 1))

    def format(self):
        formatted = [[] for __ in range(len(self.grid))]
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                formatted[y].append(Box((50 * x, y * 50, 50, 50), val, (y, x)))
        return formatted

    def update_formatted(self, val, pos):
        y, x = pos
        self.formatted[y][x].value = val

    def solve_GUI(self):
        empty = sudoku.find_empty(self.grid)
        if not empty:
            return True

        for i in range(1, 10):
            if sudoku.valid(self.grid, i, empty):
                y, x = empty
                self.grid[y][x] = i
                self.update_formatted(i, empty)
                self.formatted[y][x].correct = True
                screenUpdate()
                # pg.time.delay(10)
                
                if self.solve_GUI():
                    self.formatted[y][x].wrong = False
                    self.formatted[y][x].correct = False
                    pg.time.delay(10)
                    return True
            
                self.grid[y][x] = 0
                self.update_formatted(0, empty)
                self.formatted[y][x].wrong = True
                self.formatted[y][x].correct = False
                screenUpdate()

        return False

def screenUpdate():
    win.fill((255, 255, 255))
    for row in board.formatted:
        for box in row:
            box.draw()
    board.draw()
    pg.display.update()

run = True
board = Grid(sudoku.board1)
pencil_mode = False
selected = None

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for row in board.formatted:
                    for box in row:
                        box.highlighted = False
                        if box.rect.collidepoint(event.pos):
                            box.highlighted = True
                            selected = box

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        board.solve_GUI()
    nums = [keys[pg.K_1], keys[pg.K_2], keys[pg.K_3], keys[pg.K_4], keys[pg.K_5], keys[pg.K_6], keys[pg.K_7], keys[pg.K_8], keys[pg.K_9]]
    if any(nums):
        selected.pencil = nums.index(True) + 1
    if keys[pg.K_RETURN]:
        selected.value = selected.pencil
        y, x = selected.pos
        board.player_grid[y][x] = selected.value
        if not sudoku.valid(board.player_grid, selected.value, selected.pos):
            selected.wrong = True
        else:
            selected.wrong = False

    if keys[pg.K_p]:
        pencil_mode = not pencil_mode
    if keys[pg.K_BACKSPACE]:
        if pencil_mode:
            selected.pencil = 0
        else:
            selected.value = 0

    screenUpdate()

pg.quit()
sys.exit()
