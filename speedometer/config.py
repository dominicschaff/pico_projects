import board

PIN_I2C_SDA = board.GP0
PIN_I2C_SCL = board.GP1
PIN_MAGNETIC = board.GP2
PIN_LIGHT = board.A0
PIN_RESET = board.GP7
PIN_UNUSED = board.GP8
PIN_ERROR = board.GP16

MOTOR_ADDRESS = 0xe

WHEEL_SIZE = 1/862


# Colours:

ERR_NONE = (0, 0, 0) # black
ERR_NO_I2C = (255, 150, 0) # yellow
ERR_RUNTIME_ERROR = (0, 255, 255) # cyan
ERR_NO_SCREEN = (255, 0, 0) # red
ERR_VALUE_ERROR = (0, 255, 0) # green
ERR_NO_MOTOR = (180, 0, 255) # purple
ERR_OS_ERROR = (0, 0, 255) # blue