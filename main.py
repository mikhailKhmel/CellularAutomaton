import cellular_automation
import game
import config
import datetime


# TODO: 
# ОПТИМИЗАЦИЯ ВЫЧИСЛЕНИЙ

if config.LOG_ON:
    f = open('1.txt', 'w')

FRONT = config.FRONT
if config.WINDOW_SIZE > 1500:
    FRONT = False
PLAY = not FRONT

cell_auto = cellular_automation.CellularAutomation()
if FRONT:
    FRONT_game = game.Game()


def write_log(delta_time):
    if config.LOG_ON:
        s = f'{cell_auto.live_cells}/{abs(len(cell_auto.cells)-cell_auto.live_cells)}/{delta_time}'
        f.write(s+'\n')
        print(s+f'\tGEN: {cell_auto.generation}\t DELTA_TIME: {delta_time}')


def check_endgame():
    if cell_auto.last_snapshot == cell_auto.live_cells or cell_auto.live_cells == 0:
        exit()


def main_cycle():
    global PLAY
    while True:
        if PLAY:
            cell_auto.generation += 1

            start_time = datetime.datetime.now()

            cell_auto.calculate_cells()
            cell_auto.update_cells()
            cell_auto.update_neighbors()
            if cell_auto.generation % 200 == 0:
                cell_auto.last_snapshot = cell_auto.live_cells
            else:
                check_endgame()

            end_time = datetime.datetime.now()

            delta_time = (end_time - start_time)

            write_log(f'{delta_time.seconds}.{delta_time.microseconds}')

        if FRONT:
            FRONT_game.clock.tick(FRONT_game.FPS)
            FRONT_game.display_update()
            FRONT_game.surface.fill((FRONT_game.DEAD_COLOR))

            FRONT_game.draw_cells(cell_auto.cells)
            FRONT_game.draw_info(cell_auto.generation,
                                 cell_auto.live_cells, cell_auto.cells)
            result = FRONT_game.check_events()
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
