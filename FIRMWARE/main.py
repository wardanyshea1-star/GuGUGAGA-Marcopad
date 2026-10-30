import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.mousekeys import MouseKeys
from kmk.modules.encoder import EncoderHandler
import busio
from kmk.extensions.display import Display, SSD1306
from kmk.extensions.display.content import DisplayContent




keyboard = KMKKeyboard()
keyboard.col_pins = (board.D0, board.D1, board.D2)
keyboard.row_pins = (board.D3, board.D7, board.D8)
keyboard.diode_orientation = DiodeOrientation.ROW2COL
# Map your 3x3 layout to functions (S1 to S9)
keyboard.keymap = [
    [
        KC.LCTRL(KC.C), KC.UP,   KC.LCTRL(KC.V),  # S1 (Copy),  S2 (Up),    S3 (Paste)
        KC.LEFT,        KC.SPC,  KC.RIGHT,        # S4 (Left),  S5 (Space), S6 (Right)
        KC.MB_LCLK,     KC.DOWN, KC.MB_RCLK,           # S7 (Mouse), S8 (Down),  S9 (Mouse)
    ]
]
# Initialize the encoder handler
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# Configure encoder pins: (Pin A, Pin B, Button Pin)
encoder_handler.pins = ((board.D10, board.D6, board.D9),)

# Map rotation and button clicks: ((Counter-Clockwise, Clockwise, Button Press),)
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.MPLY),)
]
# 1. Initialize the I2C pins matching your schematic (SDA=D4, SCL=D5)
i2c_bus = busio.I2C(board.D5, board.D4)

# 2. Setup the SSD1306 OLED screen driver
display_driver = SSD1306(i2c=i2c_bus, device_address=0x3C)

# 3. Create a custom display class to calculate and show the time
class TimeDisplay(DisplayContent):
    def __init__(self):
        super().__init__()
    
    def render(self, display):
        import time
        # Get total seconds since the board started running
        total_seconds = int(time.monotonic())
        
        # Calculate hours, minutes, and seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        # Format the numbers cleanly as 00:00:00
        time_string = f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Draw the text onto the screen
        display.draw_text(0, 0, time_string)

# 4. Attach the display extension to your keyboard
keyboard.extensions.append(Display(display_driver, entries=[TimeDisplay()]))
