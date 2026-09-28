"""Configuration constants for the Pong game (Day 22)."""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_BG_COLOR = "black"
SCREEN_TITLE = "Pong Game"

# --- Paddles ---------------------------------------------------------------
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_COLOR = "white"
PADDLE_SPEED = 480
PADDLE_OFFSET_X = 350
PADDLE_HALF_WIDTH = PADDLE_WIDTH / 2
PADDLE_HALF_HEIGHT = PADDLE_HEIGHT / 2

# --- Ball ------------------------------------------------------------------
BALL_COLOR = "white"
BALL_SIZE = 1.0
BALL_BASE_RADIUS = 10  # turtle's default circle radius
BALL_RADIUS = BALL_BASE_RADIUS * BALL_SIZE
BALL_INITIAL_SPEED_X = 240
BALL_INITIAL_SPEED_Y = 240
BALL_SPEEDUP_FACTOR = 1.08
BALL_MAX_SPEED = 1080
BALL_MAX_BOUNCE_ANGLE_DEG = 60
BALL_SERVE_ANGLE_DEG = 30

# --- Net -------------------------------------------------------------------
NET_DASH_LENGTH = 15
NET_GAP_LENGTH = 15
NET_COLOR = "white"

# --- Scoreboard ------------------------------------------------------------
WINNING_SCORE = 5
SCORE_FONT = ("Courier", 24, "normal")
SCORE_GAME_OVER_FONT = ("Courier", 18, "normal")
SCORE_COLOR = "white"
SCORE_TOP_MARGIN = 60
SCORE_POSITION = (0, SCREEN_HEIGHT / 2 - SCORE_TOP_MARGIN)

# --- Timing ----------------------------------------------------------------
FRAME_DELAY = 1 / 60
MAX_DT = 0.05  # clamp delta-time to avoid large jumps

# --- Fonts -----------------------------------------------------------------
PAUSE_FONT = ("Courier", 18, "normal")
