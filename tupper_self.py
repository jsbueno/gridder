"""
The mathematical function run in the "tupper_func" can
represent an arbitrary grid of 106x17 pixels - and
what is depicted depends on the height on the Y axis modulo 17.

By calculating a sepcial - hundreds of pages long - offset on the
y axis to render, any image can be displayed.

The "default" image is the formula itself
in mathematical notation.

To learn more, check the video at:
https://www.youtube.com/watch?v=_s5RFgd59ao&fbclid=IwAR1DFQYVTHAGj_6jZG5dNsU-dAq09y-6xSyH67GveUETF20Mbnu6TieTj0E

"""

from math import floor
from decimal import Decimal as D, getcontext, setcontext
import pygame


WIDTH, HEIGTH = 1024, 768

GRAPH_WIDTH = 106

CELL_SIZE = WIDTH // GRAPH_WIDTH
REPEATS = (HEIGTH // CELL_SIZE) // 17


def init():
    global SCREEN, threshold
    con = getcontext()
    con.prec = 800
    setcontext(con)
    threshold = D(0.5)

    SCREEN = pygame.display.set_mode((WIDTH, HEIGTH))

# Number copied and pasted from the wikipedia page on the subject
# https://en.m.wikipedia.org/wiki/Tupper%27s_self-referential_formula
tupper_number = D( 960_939_379_918_958_884_971_672_962_127_852_754_715_004_339_660_129_306_651_505_519_271_702_802_395_266_424_689_642_842_174_350_718_121_267_153_782_770_623_355_993_237_280_874_144_307_891_325_963_941_337_723_487_857_735_749_823_926_629_715_517_173_716_995_165_232_890_538_221_612_403_238_855_866_184_013_235_585_136_048_828_693_337_902_491_454_229_288_667_081_096_184_496_091_705_183_454_067_827_731_551_705_405_381_627_380_967_602_565_625_016_981_482_083_418_783_163_849_115_590_225_610_003_652_351_370_343_874_461_848_378_737_238_198_224_849_863_465_033_159_410_054_974_700_593_138_339_226_497_249_461_751_545_728_366_702_369_745_461_014_655_997_933_798_537_483_143_786_841_806_593_422_227_898_388_722_980_000_748_404_719)

def tupper_func(x, y):
    exp = D(-17*floor(x)- (floor(y) % 17))
    result = floor((floor(y/17) * D(2)** exp) % 2)

    return result < threshold



def main():
    SCREEN.fill((0, 0, 0))

    offset = tupper_number

    screen_y_offset = REPEATS // 2 * 17 * CELL_SIZE
    for y in range(REPEATS // 2 * -17, REPEATS // 2 * 17):
        color = (128, 255, 255) if 0 <= y < 17 else (80, 80, 80)
        for x in range(-1, GRAPH_WIDTH + 1):
            cell = tupper_func(x, y + offset)
            if cell:
                pygame.draw.rect(SCREEN, color,
                                 (WIDTH - (x * CELL_SIZE) - 30,
                                  screen_y_offset + y * CELL_SIZE,
                                  CELL_SIZE - 1 , CELL_SIZE -1))
    pygame.display.flip()
    while True:
        pygame.event.pump()
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT or
                event.type == pygame.MOUSEBUTTONDOWN or
                event.type == pygame.KEYDOWN and event.unicode == "\x1b"
            ):
                return
        pygame.time.delay(30)



if __name__ == "__main__":
    try:
        init()
        main()
    finally:
        pygame.quit()
