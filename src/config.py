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
LANE_WIDTH = 110

KEY_BINDINGS = {
    'LANE_1': ['a'],
    'LANE_2': ['s'],
    'LANE_3': ['d'],
    'LANE_4': ['f']
}

AUDIO_FILES = [
    'src/audio/Sonne.mp3',
    'src/audio/2 minutes to midnight.mp3',
    'src/audio/Before I forget.mp3',
    'src/audio/carry on my wayward son.mp3',
    'src/audio/Hail to the king.mp3',
    'src/audio/King for a day.mp3',
    'src/audio/Its my life.mp3',
    'src/audio/Livin on a prayer.mp3',
    'src/audio/Knights of Cydonia.mp3',
    'src/audio/Seven Nation.mp3',
    'src/audio/duality.mp3',
    'src/audio/AC⚡️DC - Hells Bells.mp3',
    'src/audio/AC DC - Back In Black.mp3',
    'src/audio/Disturbed - Stricken.mp3',
    'src/audio/Europe - The Final Countdown.mp3',
    'src/audio/Iron Maiden - Run To The Hills.mp3',
    'src/audio/Kiss - Rock and Roll All Nite.mp3',
    'src/audio/Linkin Park - In the End.mp3',
    'src/audio/Linkin Park - Numb.mp3',
    'src/audio/Rammstein - Amerika.mp3',
    'Panzerkampf (Cover).mp3',
    'src/audio/Scorpions - Rock You Like A Hurricane.mp3',
    'src/audio/Scorpions - Wind Of Change.mp3'
]

BACKGROUND_IMAGES = [
    'src/scenes/spritesheet-background/akame-tatsumi.png',
    'src/scenes/spritesheet-background/spice-and-wolf.png',
    'src/scenes/spritesheet-background/fate.png',
    'src/scenes/spritesheet-background/Bocchi.png',
    'src/scenes/spritesheet-background/Magi.png',
    'src/scenes/spritesheet-background/Naruto.png',
    'src/scenes/spritesheet-background/OnePiece.png',
    'src/scenes/spritesheet-background/kimetsu.png',
    'src/scenes/spritesheet-background/FullMetalAlchemist.png',
]

INITIAL_SPAWN_INTERVAL = 2.0
MIN_SPAWN_INTERVAL = 1.0
SPAWN_INTERVAL_INCREASE = 0.0
NOTE_SPEED = 200
MAX_NOTE_SPEED = 400
NOTE_SPEED_INCREASE = 75
DIFFICULTY_INTERVAL = 10

BASE_SCORE = 100
MAX_MULTIPLIER = 6
COMBO_NEEDED = {
    1: 0,
    2: 4,
    3: 8,
    4: 12,
    5: 16,
    6: 20   
}
