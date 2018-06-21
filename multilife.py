import random
import sys
import pygame

width, height = W, H = 1024, 768
foreground = (255, 255, 255)
background = (0, 0, 0)
contour = (0, 128, 255)

FLAGS = 0 # pygame.FULLSCREEN

col, row = 64, 48
screen = pygame.display.set_mode((W, H), FLAGS)


sizex = width / col
sizey = height / row
grid_index = 0
paused = False


class GameOver(Exception):
    pass


class Grid(dict):
    survive = (2, 3)
    born = (3,)
    color = (0, 0, 0)
    
    def __init__(self, color, survive=None, born=None):
        self.color = color
        self.survive = self.survive if survive is None else survive
        self.born = self.born if born is None else born
        
    def __iter__(self):
        for x in range(col):
            for y in range(row):
                yield (x,y), self[x,y]

    def __missing__(self, index):
        return 0

    def neighbour_count(self, coords):
        x, y = coords
        total = 0
        for c in [(x - 1, y - 1), (x, y - 1), (x + 1, y -1),
                  (x - 1, y), (x + 1, y),
                  (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]:
            total += self[c]
        return total

    def update_cells(self):

        new_grid = dict()
        for coord, element in self:
            n = self.neighbour_count(coord)
            if (element and n in self.survive) or n in self.born:
                new_grid[coord] = 1
        self.clear()
        self.update(new_grid)


grids = [Grid((255, 0, 0)), Grid((0, 255, 0)), Grid((0, 0, 255)), Grid((255, 128, 0)), Grid((255, 255, 255))]


def square(coord, color):
    x, y = coord

    pygame.draw.rect(screen, color, (x * sizex, y * sizey, sizex, sizey))
    pygame.draw.rect(screen, contour, (x * sizex, y * sizey, sizex, sizey), 2)


def populate():
    if len(sys.argv) < 2:
        print("Put a coeficient as parameter if you want to randomly pre-populate the grids")
        return

    threshold = float(sys.argv[1])
    
    for grid in grids:
        for coord, elemento in grid:
             grid[coord] = random.random() < threshold


def draw():
    screen.fill(background)
    colors = [grid.color for grid in grids]
    for cells in zip(*grids):
        coord = cells[0][0]
        color = tuple(min(255, sum(cell[1] * color[component] for cell, color in zip(cells, colors)))  for component in (0,1,2))
        square(coord, color)
    pygame.display.flip()




def click(event):

    buttons = event.buttons[0] if hasattr(event, "buttons") else event.button == 1
    if not buttons:
        return

    pixel_coord = event.pos
    px, py = pixel_coord
    x = px // sizex
    y = py // sizey
    if event.type == pygame.MOUSEMOTION:
        grids[grid_index][x, y] = 1
    else:
        grids[grid_index][x, y] ^= 1


def main():
    global paused, grid_index
    populate()
    while True:
        pygame.event.pump()
        for event in pygame.event.get():

            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == 0x1b:
                raise GameOver
            elif event.type == pygame.KEYDOWN and event.unicode == "p":
                paused = not paused
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                click(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    grid_index = (grid_index + 1) % len(grids)
        draw()
        for grid in grids:
            if not paused:
                grid.update_cells()
        pygame.time.delay(125)


try:
    main()
except GameOver:
    pass
finally:
    pygame.quit()
