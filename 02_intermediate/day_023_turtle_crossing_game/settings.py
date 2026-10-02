"""Configuration constants for the Turtle Crossing game (Day 23)."""

# --- SCREEN ------------------------------------------------------------------
SCREEN_W = 600
SCREEN_H = 600
SCREEN_BG = "white"
SCREEN_TITLE = "Turtle Crossing Game"
SCREEN_TRACER = 0  # 0 disables automatic animation

# --- PLAYER ------------------------------------------------------------------
PLAYER_SPEED = 0  # 0 = no turtle animation delay
PLAYER_STEP = 20
PLAYER_COLOR = "green"
PLAYER_HEADING = 90
PLAYER_START_POSITION = (0, -SCREEN_H / 2 + 20)
PLAYER_FINISH_LINE_Y = SCREEN_H / 2 - 40
PLAYER_W = 20
PLAYER_H = 20

# --- CAR ---------------------------------------------------------------------
CAR_COLORS = ["red", "yellow", "blue", "brown", "orange", "black"]
CAR_SPEED = 0  # 0 = no turtle animation delay
CAR_MIN_MOVE_SPEED = 200
CAR_MAX_MOVE_SPEED = 400
CAR_HEADING = 180
CAR_W = 40
CAR_H = 20

# --- CAR MANAGER -------------------------------------------------------------
CAR_MANAGER_CAR_START_POSITION_X = SCREEN_W + 20
CAR_MANAGER_MIN_CAR_START_POSITION_Y = -SCREEN_H / 2 + 20
CAR_MANAGER_MAX_CAR_START_POSITION_Y = SCREEN_H / 2 - 20
CAR_MANAGER_MIN_SPAWN_DELAY = 0.15
CAR_MANAGER_MAX_SPAWN_DELAY = 0.6
CAR_MANAGER_SPAWN_DELAY_FLOOR = 0.05
CAR_MANAGER_LEVEL_SPAWN_DECAY = 0.85

# --- HUD ---------------------------------------------------------------------
HUD_COLOR = "black"
HUD_FONT = ("Arial", 16, "normal")
HUD_MESSAGE_FONT = ("Arial", 14, "normal")
HUD_LEVEL_POSITION = (-SCREEN_W / 2 + 10, SCREEN_H / 2 - 40)
HUD_MESSAGE_POSITION = (0, 0)

# --- TIMING ------------------------------------------------------------------
FRAME_DELAY = 1 / 60
MAX_DT = 0.05
