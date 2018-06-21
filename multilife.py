import random
import pygame

width, height = W, H = 1024, 768
foreground = (255, 255, 255)
background = (0, 0, 0)
contour = (0, 128, 255)

LIVE = (2, 3)
BORN = (3,)
FLAGS = 0 # pygame.FULLSCREEN

col, row = 64, 48
screen = pygame.display.set_mode((W, H), FLAGS)


sizex = width / col
sizey = height / row
color_index = 0
paused = False


class GameOver(Exception):
    pass


class Grid(dict):
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


grids = [Grid(), Grid(), Grid()]


def square(coord, cor):
    x, y = coord

    pygame.draw.rect(screen, cor, (x * sizex, y * sizey, sizex, sizey))
    pygame.draw.rect(screen, contour, (x * sizex, y * sizey, sizex, sizey), 2)


def populate():
    for grid in grids:
        for coord, elemento in grid:
             grid[coord] = random.random() < 0.1


def draw():
    screen.fill(background)
    for rc, gc, bc in zip(*grids):
        coord = rc[0]
        r = rc[1]; g = gc[1]; b = bc[1]
        cor = (255 * r, 255 * g, 255 * b)
        square(coord, cor)
    pygame.display.flip()


def update(grid):

    nova_grid = Grid()
    for coord, elemento in grid:
        n = grid.neighbour_count(coord)
        if elemento and n in LIVE or n in BORN:
            nova_grid[coord] = 1
    grid.clear()
    grid.update(nova_grid)


def click(event):

    buttons = event.buttons[0] if hasattr(event, "buttons") else event.button == 1
    if not buttons:
        return

    pixel_coord = event.pos
    px, py = pixel_coord
    x = px // sizex
    y = py // sizey
    if event.type == pygame.MOUSEMOTION:
        grids[color_index][x, y] = 1
    else:
        grids[color_index][x, y] ^= 1


def main():
    global paused, color_index
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
                    color_index = (color_index + 1) % 3
        draw()
        for grid in grids:
            if not paused:
                update(grid)
        pygame.time.delay(125)


try:
    main()
except GameOver:
    pass
finally:
    pygame.quit()
