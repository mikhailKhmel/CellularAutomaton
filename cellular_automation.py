from configparser import ConfigParser
import random
from cell import Cell

config = ConfigParser()
config.read('settings.conf')


class CellularAutomation:
    WINDOW_SIZE = int(config['Default']['window_size'])
    CELL_SIZE = int(config['Default']['cell_size'])
    WIDTH = WINDOW_SIZE // CELL_SIZE
    cells: dict
    last_snapshot = {}
    generation = 0
    live_cells = 0
    rule = config['Default']['rule']

    def __init__(self):
        self.cells = {
            j + self.WIDTH * i: Cell(i, j) for i in range(self.WIDTH) for j in range(self.WIDTH)}

        if config['Default'].getboolean('random_cells'):
            self.make_random_cells()

    def make_random_cells(self):
        self.clean_cells()
        for i in range(len(self.cells)//2):
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
                    if i < 0:
                        i = self.WIDTH - 1
                    elif i > self.WIDTH:
                        i = 0

                    if j < 0:
                        j = self.WIDTH - 1
                    elif j > self.WIDTH:
                        j = 0

                    curr_id = j + self.WIDTH * i
                    try:
                        if self.cells[curr_id].status:
                            count += 1
                    except:
                        pass
        return count

    def update_cells(self):
        rule_sections = self.rule.split('/')
        b = rule_sections[0].split(',')
        s = rule_sections[1].split(',')
        for key, item in self.cells.items():
            if self.cells[key].status:
                if not (str(item.neighbors_count) in s):
                    self.cells[key].status = False
            else:
                if str(item.neighbors_count) in b:
                    self.cells[key].status = True
        # self.update_neighbors()

    def clean_cells(self):
        self.cells = {
            j + self.WIDTH * i: Cell(i, j) for i in range(self.WIDTH) for j in range(self.WIDTH)}

    def calculate_cells(self):
        self.live_cells = 0
        for cell in self.cells.values():
            if cell.status:
                self.live_cells += 1
