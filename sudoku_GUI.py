import pygame as pg
import sudoku

pg.init()
win = pg.display.set_mode((450, 500))
pg.display.set_caption('Sudoku Solver')
enterFont = pg.font.Font('Raleway-VariableFont_wght.ttf', 30)

class Box():
    def __init__(self, rect, value):
        self.rect = rect
        self.value = value
        self.pencil = 0

    def draw(self):
        pg.draw.rect(win, (0, 0, 0), self.rect, 1)
        if self.value != 0:
            number_surface = enterFont.render(str(self.value), True, (0, 0, 0))
            number_rect = number_surface.get_rect(center=(self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2))
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
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    screenUpdate(makeGrid(sudoku.board))

pg.quit()
