# Cellular Automaton
A cellular automaton written entirely in `python3`. This project is aimed at studying the behavior of cellular automata under different "rules of the game". To customize and configure the machine, a special configuration file is used: `settings.conf`.

The program consists of two main modules: "Core" and "Front". The kernel is responsible for all calculations of each of the generations of the machine, based on the "rules" set by the user.

The front is responsible for the visual display of the cell field. Depending on the settings, the module applies colors for "live" and "dead" cells, window size, cell size, font size (there is a display of the current generation, the number of "live" and "dead" cells). Due to the modular structure, if desired, the Front module can be disabled in the configuration file. Using the mouse, you can change the state of the cell to the opposite.

To start the machine with the Front on, use the `SPACE` key.

With the Front disabled, the vending machine will start automatically.

---
![Start Window](assets/images/start_window.png)
![In The Process](assets/images/in_process.png)

---

## Full list of settings:


`[CORE]`
- `RANDOM_CELLS` = Generation of random "live" cells when the machine starts.
- `RULE` = Machine conditions. It is set as follows: Birth / Survival. The number of neighbors at which the cell is born and the number at which the cell continues to exist are listed separated by commas. For example, the famous game "Life" works according to the 3 / 2,3 rule.
- `RECORD` = Record the state of each generation to a log file (record.log). 1 - on, 0 - off.

`[FRONT]`
- `FRONT` = enable or disable the front module. 1 - on, 0 - off.
- `WINDOW_SIZE` = SQUARE window size in pixels
- `CELL_SIZE` = SQUARE cell size in pixels
- `FONT_SIZE` = font size
- `LIVE_COLOR` = live cell color in RGB (255,255,255)
- `DEAD_COLOR` = RGB dead cell color (0,0,0)

## DEPENDENCIES
The program works without dependencies if FRONT is disabled. Otherwise, the `pygame` library is needed.
 
### Enjoy!