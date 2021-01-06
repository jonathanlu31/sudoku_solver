import sys
import copy
import pygame as pg
import sudoku

pg.init()
win = pg.display.set_mode((450, 500))
pg.display.set_caption('Sudoku Solver')
enterFont = pg.font.Font('SourceSansPro-Regular.ttf', 30)
pencilFont = pg.font.Font('SourceSansPro-Regular.ttf', 15)


class Box():
    def __init__(self, rect, value, pos, fixed):
        self.rect = pg.Rect(rect)
        self.value = value
        self.pencil = 0
        self.highlighted = False
        self.correct = False
        self.wrong = False
        self.pos = pos
        self.fixed = fixed

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
        if self.pencil != 0:
            pencil_surface = pencilFont.render(str(self.pencil), True, (0, 0, 0, 0.7))
            pencil_rect = pencil_surface.get_rect(topleft=(self.rect.x + 7, self.rect.y + 3))
            win.blit(pencil_surface, pencil_rect)


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
                if val != 0:
                    formatted[y].append(Box((50 * x, y * 50, 50, 50), val, (y, x), True))
                else:
                    formatted[y].append(Box((50 * x, y * 50, 50, 50), val, (y, x), False))
        return formatted

    def update_formatted(self, val, pos):
        y, x = pos
        self.formatted[y][x].value = val

    def solve_gui(self):
        empty = sudoku.find_empty(self.grid)
        if not empty:
            return True

        for i in range(1, 10):
            if sudoku.valid(self.grid, i, empty):
                y, x = empty
                self.grid[y][x] = i
                self.update_formatted(i, empty)
                self.formatted[y][x].correct = True
                screen_update()
                
                if self.solve_gui():
                    self.formatted[y][x].wrong = False
                    self.formatted[y][x].correct = False
                    pg.time.delay(10)
                    return True
            
                self.grid[y][x] = 0
                self.update_formatted(0, empty)
                self.formatted[y][x].wrong = True
                self.formatted[y][x].correct = False
                screen_update()

        return False


def draw_timer():
    sec = pg.time.get_ticks() // 1000
    minutes = (sec // 60 if sec >= 60 else 0)
    time_surface = enterFont.render(f'{minutes:02}:{sec - minutes * 60:02}', True, (0, 0, 0))
    time_rect = time_surface.get_rect(topleft=(360, 455))
    win.blit(time_surface, time_rect)


def screen_update():
    win.fill((255, 255, 255))
    for row in play_board.formatted:
        for box in row:
            box.draw()
    play_board.draw()
    draw_timer()
    pg.display.update()


if len(sys.argv) > 1:
    difficulty = sys.argv[1]
    if difficulty == 'medium':
        board = sudoku.board2
    elif difficulty == 'hard':
        board = sudoku.board3
    elif difficulty == 'expert':
        board = sudoku.board4
    else:
        board = sudoku.board1
else:
    board = sudoku.board1

run = True
play_board = Grid(board)
pencil_mode = False
selected = None

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for row in play_board.formatted:
                    for box in row:
                        box.highlighted = False
                        if box.rect.collidepoint(event.pos):
                            box.highlighted = True
                            selected = box

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        play_board.solve_gui()
    nums = [keys[pg.K_1], keys[pg.K_2], keys[pg.K_3],
            keys[pg.K_4], keys[pg.K_5], keys[pg.K_6],
            keys[pg.K_7], keys[pg.K_8], keys[pg.K_9]]
    if selected and not selected.fixed:
        if any(nums):
            selected.pencil = nums.index(True) + 1
        if keys[pg.K_RETURN] and selected.pencil:
            selected.value = selected.pencil
            selected.pencil = 0
            y, x = selected.pos
            play_board.player_grid[y][x] = selected.value
            if not sudoku.valid(play_board.player_grid, selected.value, selected.pos):
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

    screen_update()

pg.quit()
sys.exit()
