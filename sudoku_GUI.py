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

    def draw(self):
        pg.draw.rect(win, (0, 0, 0), self.rect, 1)
        if self.highlighted:
            pg.draw.rect(win, (187, 222, 251), (self.rect.x + 1, self.rect.y + 1, 48, 48))
        if self.value != 0:
            number_surface = enterFont.render(str(self.value), True, (0, 0, 0))
            number_rect = number_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            win.blit(number_surface, number_rect)

def makeGrid(grid):
    formatted_grid = []
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            formatted_grid.append(Box((50 * x, y * 50, 50, 50), val))
    return formatted_grid

def screenUpdate(grid):
    win.fill((255, 255, 255))
    for box in grid:
        box.draw()
    pg.display.update()

run = True
grid = makeGrid(sudoku.board)
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for box in grid:
                    box.highlighted = False
                    if box.rect.collidepoint(event.pos):
                        box.highlighted = True

    screenUpdate(grid)

pg.quit()
sys.exit()
