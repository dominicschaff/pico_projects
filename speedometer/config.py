import board

PIN_I2C_SDA = board.GP0
PIN_I2C_SCL = board.GP1
PIN_MAGNETIC = board.GP2
PIN_LIGHT = board.A0
PIN_RESET = board.GP7
PIN_UNUSED = board.GP8
PIN_ERROR = board.GP16
PIN_WP_MEMORY = board.GP5

MOTOR_ADDRESS = 0xe

WHEEL_SIZE = 1.0/862.0

RESET_TIME = 5_000

UPDATE_INTERVAL = 1_000


# Colours:

ERR_NONE          = (  0,   0,   0) # black
ERR_NO_SCREEN     = (255,   0,   0) # red
ERR_VALUE_ERROR   = (  0, 255,   0) # green
ERR_OS_ERROR      = (  0,   0, 255) # blue
ERR_NO_MOTOR      = (255,   0, 255) # pink
ERR_NO_STORAGE    = (255, 255,   0) # orange
ERR_RUNTIME_ERROR = (  0, 255, 255) # cyan
ERR_NO_I2C        = (255, 255, 255) # white

# State
STATE_FILE = "/data.json"
STATE_MINIMUM_DURATION = 60_000
STATE_MINIMUM_DISTANCE = 0.5