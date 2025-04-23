SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Guitar Hero"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

NUM_LANES = 4
LANE_COLORS = [RED, GREEN, YELLOW, BLUE]
LANE_WIDTH = 100

KEY_BINDINGS = {
    'LANE_1': ['a', 'left'],
    'LANE_2': ['s', 'down'],
    'LANE_3': ['d', 'up'],
    'LANE_4': ['f', 'right']
}

INITIAL_SPAWN_INTERVAL = 2.0
MIN_SPAWN_INTERVAL = 2.0
SPAWN_INTERVAL_DECREASE = 0.0
NOTE_SPEED = 200              

BASE_SCORE = 100              
MAX_MULTIPLIER = 6            
COMBO_NEEDED = {             
    1: 0,   
    2: 8,    
    3: 16,   
    4: 24,   
    5: 32,   
    6: 40    
}
