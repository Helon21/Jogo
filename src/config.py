SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Guitar Hero - Anime Edition"

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
    'src/audio/2_minutes_to_midnight.mp3',
    'src/audio/Before_I_forget.mp3',
    'src/audio/carry_on_my_wayward_son.mp3',
    'src/audio/Hail_to_the_king.mp3',
    'src/audio/King_for_a_day.mp3',
    'src/audio/Its_my_life.mp3',
    'src/audio/Livin_on_a_prayer.mp3',
    'src/audio/Knights_of_Cydonia.mp3',
    'src/audio/Seven_Nation.mp3',
    'src/audio/duality.mp3',
    'src/audio/ACDC_Hells_Bells.mp3',
    'src/audio/ACDC_Back_In_Black.mp3',
    'src/audio/Disturbed_Stricken.mp3',
    'src/audio/Europe_The_Final_Countdown.mp3',
    'src/audio/Iron_Maiden_Run_To_The_Hills.mp3',
    'src/audio/Kiss_Rock_and_Roll_All_Nite.mp3',
    'src/audio/Linkin_Park_In_the_End.mp3',
    'src/audio/Linkin_Park_Numb.mp3',
    'src/audio/Rammstein_Amerika.mp3',
    'src/audio/Panzerkampf_Cover.mp3',
    'src/audio/Scorpions_Rock_You_Like_A_Hurricane.mp3',
    'src/audio/Scorpions_Wind_Of_Change.mp3',
    'src/audio/Breaking_the_Habit.mp3',
    'src/audio/Nirvana_Smells_Like_Teen_Spirit.mp3',
    'src/audio/Three_Days_Grace_I_Hate_Everything_About_You.mp3',
    'src/audio/Daft_Punk_Get_Lucky.mp3',
    'src/audio/Metallica_Master_of_Puppets.mp3',
    'src/audio/Guns_N_Roses_Sweet_Child_O_Mine.mp3',
    'src/audio/Meg_and_Dia_Monster.mp3',
    'src/audio/Evanescence_Everybodys_Fool.mp3',
    'src/audio/Guns_N_Roses_Paradise_City.mp3',
    'src/audio/Crawling_Linkin_Park.mp3',
    'src/audio/The_Emptiness_Machine_Linkin_Park.mp3'
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

MENU_TITLE_SIZE = 72
MENU_BUTTON_FONT_SIZE = 32
MENU_MUSIC_FONT_SIZE = 20
MENU_INSTRUCTION_FONT_SIZE = 16

MENU_BUTTON_HOVER_GREEN = (0, 200, 0)
MENU_BUTTON_HOVER_RED = (200, 0, 0)