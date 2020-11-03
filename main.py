import sys
import cellular_automation
import game

from configparser import ConfigParser

config = ConfigParser()
config.read('settings.conf')

log_on = config['Default'].getboolean('log_on')
if log_on:
    f = open('1.txt', 'w')


FRONT = False
PLAY = not FRONT

cell_auto = cellular_automation.CellularAutomation()
if FRONT:
    front_game = game.Game()


def write_log():
    if log_on:
        s = f'{cell_auto.live_cells}/{abs(len(cell_auto.cells)-cell_auto.live_cells)}'
        f.write(s+'\n')
        print(s+'\tGEN: %s' % cell_auto.generation)


def check_endgame():
    if cell_auto.last_snapshot == cell_auto.live_cells or cell_auto.live_cells == 0:
        exit()


def main_cycle():
    global PLAY
    while True:
        if PLAY:
            cell_auto.generation += 1

            cell_auto.calculate_cells()
            cell_auto.update_cells()
            cell_auto.update_neighbors()
            if cell_auto.generation % 200 == 0:
                cell_auto.last_snapshot = cell_auto.live_cells
            else:
                check_endgame()

            write_log()

        if FRONT:
            front_game.clock.tick(front_game.FPS)
            front_game.display_update()
            front_game.surface.fill((front_game.DEAD_COLOR))

            front_game.draw_cells(cell_auto.cells)
            front_game.draw_info(cell_auto.generation,
                                 cell_auto.live_cells, cell_auto.cells)
            result = front_game.check_events()
            if result[0] == 'PLAY_UPDATE':
                PLAY = not PLAY
            elif result[0] == 'NEIGHBORS_UPDATE':
                cell_auto.cells[result[1][1] + result[1][0] * cell_auto.WIDTH].status = True if not cell_auto.cells[result[1][1] +
                                                                               result[1][0] * cell_auto.WIDTH].status else False
                cell_auto.update_neighbors()


def main():
    main_cycle()


if __name__ == "__main__":
    main()
