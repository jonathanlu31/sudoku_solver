import sys
import pygame as pg
import sudoku

pg.init()
win = pg.display.set_mode((450, 500))
pg.display.set_caption('Sudoku Solver')
enterFont = pg.font.Font('Raleway-VariableFont_wght.ttf', 30)

class Box():
    def __init__(self, rect, value):
        self.rect = pg.Rect(rect)
        self.value = value
        self.pencil = 0
        self.highlighted = False
        self.visited = False
        self.correct = False
        self.wrong = False

    def draw(self):
        pg.draw.rect(win, (0, 0, 0), self.rect, 1)
        if self.highlighted:
            pg.draw.rect(win, (187, 222, 251), (self.rect.x + 1, self.rect.y + 1, 48, 48))
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
        self.formatted = self.format()

    def format(self):
        formatted = [[] for __ in range(len(self.grid))]
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                formatted[y].append(Box((50 * x, y * 50, 50, 50), val))
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
                
                pg.time.delay(100)
                if self.solve_GUI():
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
    pg.display.update()

run = True
board = Grid(sudoku.board)
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
    
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        board.solve_GUI()

    screenUpdate()

pg.quit()
sys.exit()
