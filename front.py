import sys
import pygame
import config


FONT_SIZE = config.FONT_SIZE


class Game:
    FPS = 30
    WINDOW_SIZE = config.WINDOW_SIZE
    CELL_SIZE = config.CELL_SIZE
    LIVE_COLOR = config.LIVE_COLOR
    DEAD_COLOR = config.DEAD_COLOR
    play = False

    def __init__(self):
        pygame.init()
        self.font_pygame = pygame.font.SysFont('Arial', FONT_SIZE)
        self.surface = pygame.display.set_mode(
            (self.WINDOW_SIZE+300, self.WINDOW_SIZE))
        self.clock = pygame.time.Clock()

    def draw_cells(self, cells):
        for i in range(len(cells)):
            if cells[i].status:
                pygame.draw.rect(self.surface, self.LIVE_COLOR, (cells[i].x*self.CELL_SIZE,
                                                                 cells[i].y *
                                                                 self.CELL_SIZE,
                                                                 self.CELL_SIZE,
                                                                 self.CELL_SIZE))

    def draw_info(self, generation, live_cells, cells):
        info_sc = pygame.Surface((300, self.WINDOW_SIZE))
        info_sc.fill(self.DEAD_COLOR)
        text_gen = self.font_pygame.render(
            "GENERATION: " + str(generation), 1, self.LIVE_COLOR)
        text_count_cells = self.font_pygame.render(
            "ALIVE CELLS: " + str(live_cells), 1, self.LIVE_COLOR)
        text_count_cells1 = self.font_pygame.render(
            "DEAD CELLS: " + str(abs(len(cells)-live_cells)), 1, self.LIVE_COLOR)

        info_sc.blit(text_gen, (0, 0))
        info_sc.blit(text_count_cells, (0, FONT_SIZE))
        info_sc.blit(text_count_cells1, (0, FONT_SIZE*2))

        self.surface.blit(info_sc, (self.WINDOW_SIZE, 0))

    def check_events(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    return ['PLAY_UPDATE']
            elif i.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = (pos[0] // self.CELL_SIZE, pos[1] // self.CELL_SIZE)
                return ['NEIGHBORS_UPDATE', pos]
        return ['']

    def display_update(self):
        pygame.display.update()
