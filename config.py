from configparser import ConfigParser

config = ConfigParser()
config.read('settings.conf')

RECORD = config['CORE'].getboolean('RECORD')
FONT_SIZE = int(config['FRONT']['FONT_SIZE'])
WINDOW_SIZE = int(config['FRONT']['WINDOW_SIZE'])
CELL_SIZE = int(config['FRONT']['CELL_SIZE'])
RULE = config['CORE']['RULE']
RANDOM_CELLS = config['CORE'].getboolean('RANDOM_CELLS')
FRONT = config['FRONT'].getboolean('FRONT')
LIVE_COLOR = eval(config['FRONT']['LIVE_COLOR'])
DEAD_COLOR = eval(config['FRONT']['DEAD_COLOR'])