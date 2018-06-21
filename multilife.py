import random
import pygame

larg, alt = W, H = 1024, 768
frente = (255, 255, 255)
fundo = (0, 0, 0)
contorno = (0, 128, 255)

VIVE = (2, 3)
NASCE = (3,)
FLAGS = 0 # pygame.FULLSCREEN

col, lin = 64, 48
tela = pygame.display.set_mode((W, H), FLAGS)


tamx = larg / col
tamy = alt / lin

class Grade(dict):
    def __iter__(self):
        for x in range(col):
            for y in range(lin):
                yield (x,y), self[x,y]

    def __missing__(self, index):
        return 0

    def conta_vizinhos(self, coords):
        x, y = coords
        total = 0
        for c in [(x - 1, y - 1), (x, y - 1), (x + 1, y -1),
                  (x - 1, y), (x + 1, y),
                  (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]:
            total += self[c]
        return total

grades = [Grade(), Grade(), Grade()]

# A função quadrado faz todas as contas de coordenadas

def quadrado(coord, cor):
    x, y = coord

    pygame.draw.rect(tela, cor, (x * tamx, y * tamy, tamx, tamy))
    pygame.draw.rect(tela, contorno, (x * tamx, y * tamy, tamx, tamy), 2)

def cria():
    for grade in grades:
        for coord, elemento in grade:
             grade[coord] = random.random() < 0.1

def desenha():
    tela.fill(fundo)
    for rc, gc, bc in zip(*grades):
        coord = rc[0]
        r = rc[1]; g = gc[1]; b = bc[1]
        cor = (255 * r, 255 * g, 255 * b)
        quadrado(coord, cor)
    pygame.display.flip()

class GameOver(Exception):
    pass

def atualiza(grade):

    nova_grade = Grade()
    for coord, elemento in grade:
        n = grade.conta_vizinhos(coord)
        if elemento and n in VIVE or n in NASCE:
            nova_grade[coord] = 1
    grade.clear()
    grade.update(nova_grade)

color_index = 0
def click(event):

    if not event.buttons[0]:
        return

    pixel_coord = event.pos
    px, py = pixel_coord
    x = px // tamx
    y = py // tamy
    grades[color_index][x, y] = 1

paused = False
def principal():
    global paused, color_index
    cria()
    while True:
        pygame.event.pump()
        for event in pygame.event.get():

            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == 0x1b:
                raise GameOver
            elif event.type == pygame.KEYDOWN and event.unicode == "P":
                paused = not paused
            elif event.type == pygame.MOUSEMOTION:
                click(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    color_index = (color_index + 1) % 3
        desenha()
        for grade in grades:
            if not paused:
                atualiza(grade)
        pygame.time.delay(125)

try:
    principal()
except GameOver:
    pass
finally:
    pygame.quit()
