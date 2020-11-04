from configparser import ConfigParser

config = ConfigParser()
config.read('settings.conf')

LOG_ON = config['CELL_AUTO'].getboolean('LOG_ON')
FONT_SIZE = int(config['FRONT']['FONT_SIZE'])
FPS = int(config['FRONT']['SPEED'])
WINDOW_SIZE = int(config['FRONT']['WINDOW_SIZE'])
CELL_SIZE = int(config['FRONT']['CELL_SIZE'])
RULE = config['CELL_AUTO']['RULE']
RANDOM_CELLS = config['CELL_AUTO'].getboolean('RANDOM_CELLS')
FRONT = config['FRONT'].getboolean('FRONT')
LIVE_COLOR = eval(config['FRONT']['LIVE_COLOR'])
DEAD_COLOR = eval(config['FRONT']['DEAD_COLOR'])