import sys
import pygame
import configparser

config = configparser.ConfigParser()
config.read('settings.conf')


font_size = int(config['Default']['font_size'])



# TODO: рефакторинг
# разделить процесс подсчета новых поколений и отображение (pygame)
# повзолит ускорить анализ результатов т.к. не понадобится отображение
# в бэкенде (подсчет новых поколений) реализовать возомжность применять рандомные правила rules[512]
#

class Game:
    FPS = int(config['Default']['speed'])
    WINDOW_SIZE = int(config['Default']['window_size'])
    CELL_SIZE = int(config['Default']['cell_size'])
    LIVE_COLOR = (0, 0, 0)
    DEAD_COLOR = (255, 255, 255)
    play = False

    def __init__(self):
        pygame.init()
        self.font_pygame = pygame.font.SysFont('Arial', font_size)
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
        info_sc.blit(text_count_cells, (0, font_size))
        info_sc.blit(text_count_cells1, (0, font_size*2))

        self.surface.blit(info_sc, (self.WINDOW_SIZE, 0))

    def check_events(self):
        for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        return ['PLAY_UPDATE']
                        #PLAY = False if PLAY else True
                elif i.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    pos = (pos[0] // self.CELL_SIZE, pos[1] // self.CELL_SIZE)
                    try:
                        # cells[pos[1] + pos[0] * self.WIDTH].status = True if not cells[pos[1] +
                        #                                                                          pos[0] * self.WIDTH].status else False
                        return ['NEIGHBORS_UPDATE', pos]
                    except:
                        pass
        return ['']
    
    def display_update(self):
        pygame.display.update()