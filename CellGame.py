import pygame
import random
import sys
import configparser

config = configparser.ConfigParser()
config.read('settings.conf')

pygame.init()
font_size = int(config['Default']['font_size'])
font_pygame = pygame.font.SysFont('Arial', font_size)



class Cell:
    x: int
    y: int
    status: bool  # false - died, true - alive
    neighbors_count: int

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = False
        self.neighbors_count = 0

    def dump(self):
        return {"x": self.x, "y": self.y, "status": self.status, "neighbors_count": self.neighbors_count}

# TODO: организовать точную настройку автомата
# добавить возможность вручную регулировать правила автомата
# отображение информации:
#   - количество живых и мертвых клеток
#   - текущее правило
#   - текущее поколение


class Game:
    WINDOW_SIZE = int(config['Default']['window_size'])
    CELL_SIZE = int(config['Default']['cell_size'])
    width = WINDOW_SIZE // CELL_SIZE
    FPS = 100

    LIVE_COLOR = (0, 0, 0)
    DEAD_COLOR = (255, 255, 255)

    play = False

    cells: dict
    generation = 0
    live_cells = 0

    def __init__(self, rule: dict):
        self.birth_rule = rule['B']
        self.survival_rule = rule['S']
        self.surface = pygame.display.set_mode(
            (self.WINDOW_SIZE+300, self.WINDOW_SIZE))
        self.clock = pygame.time.Clock()
        self.cells = {
            j + self.width * i: Cell(i, j) for i in range(self.width) for j in range(self.width)}
        if config['Default'].getboolean('random_cells'):
            self.make_random_cells()

        self.main_cycle()

    def clean_cells(self):
        self.cells = {
            j + self.width * i: Cell(i, j) for i in range(self.width) for j in range(self.width)}

    def make_random_cells(self):
        self.clean_cells()
        for i in range(int(len(self.cells) / 2)):
            random_id = random.randint(0, len(self.cells) - 1)
            self.cells[random_id].status = True
        self.update_neighbors()

    def update_neighbors(self):
        for curr_cell in self.cells.keys():
            self.cells[curr_cell].neighbors_count = self.get_neighbors_count(self.cells[curr_cell].x,
                                                                             self.cells[curr_cell].y)

    def get_neighbors_count(self, current_x: int, current_y: int) -> int:
        count = 0
        for i in range(current_x - 1, current_x + 2):
            for j in range(current_y - 1, current_y + 2):
                if (i == current_x) and (j == current_y):
                    pass
                else:
                    if i < 0 or j < 0 or i > self.width or j > self.width:
                        continue
                    else:
                        curr_id = j + self.width * i
                        try:
                            if self.cells[curr_id].status:
                                count += 1
                        except:
                            pass
        return count

    def update_cells(self):
        for key, item in self.cells.items():
            if self.cells[key].status:
                if item.neighbors_count < 2 or item.neighbors_count > 3:
                    self.cells[key].status = False
            else:
                if item.neighbors_count == 3:
                    self.cells[key].status = True
        self.update_neighbors()

    def draw_cells(self):
        for i in range(len(self.cells)):
            if self.cells[i].status:
                pygame.draw.rect(self.surface, self.LIVE_COLOR, (self.cells[i].x*self.CELL_SIZE,
                                                                 self.cells[i].y *
                                                                 self.CELL_SIZE,
                                                                 self.CELL_SIZE,
                                                                 self.CELL_SIZE))
    
    def draw_info(self):
        info_sc = pygame.Surface((300,self.WINDOW_SIZE))
        info_sc.fill(self.DEAD_COLOR)
        text_gen = font_pygame.render("GENERATION: " + str(self.generation), 1, self.LIVE_COLOR)
        text_count_cells = font_pygame.render("ALIVE CELLS: " + str(self.live_cells), 1, self.LIVE_COLOR)
        text_count_cells1 = font_pygame.render("DEAD CELLS: " + str(abs(len(self.cells)-self.live_cells)), 1, self.LIVE_COLOR)

        info_sc.blit(text_gen, (0,0))
        info_sc.blit(text_count_cells, (0,font_size))
        info_sc.blit(text_count_cells1, (0,font_size*2))

        self.surface.blit(info_sc, (self.WINDOW_SIZE,0))
    
    def calculate_cells(self):
        self.live_cells=0
        for cell in self.cells.values():
            if cell.status:
                self.live_cells+=1


    def main_cycle(self):
        while True:
            self.clock.tick(self.FPS)
            pygame.display.update()
            self.surface.fill((self.DEAD_COLOR))
            
            self.draw_cells()
            self.draw_info()

            if self.play:
                self.generation+=1
                self.calculate_cells()
                self.update_cells()

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        self.play = False if self.play else True
                elif i.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    pos = (pos[0] // self.CELL_SIZE, pos[1] // self.CELL_SIZE)
                    try:
                        self.cells[pos[1] + pos[0] * self.width].status = True if not self.cells[pos[1] +
                                                                                             pos[0] * self.width].status else False
                        self.update_neighbors()
                    except:
                        pass


rule = {'B': '3', 'S': '2,3'}
game = Game(rule)
