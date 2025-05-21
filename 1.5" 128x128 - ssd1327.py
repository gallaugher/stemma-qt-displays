# Creates a pulsing set of rings under text.
import time
import math
import board
import displayio
import busdisplay
import i2cdisplaybus
import terminalio
from adafruit_display_text import label
import adafruit_ssd1327

# === Try to import bitmap fonts for better readability ===
try:
    from adafruit_bitmap_font import bitmap_font
    # Load a built-in font with variable width characters
    font = bitmap_font.load_font("/fonts/Arial_Bold_12.bdf")  # If you've uploaded this font
    # Or try the built-in fonts
    # font = bitmap_font.load_font("/fonts/Arial-Bold-12.pcf")  # Common built-in font
    USING_CUSTOM_FONT = True
except (ImportError, OSError):
    # Fall back to terminalio if custom font fails
    font = terminalio.FONT
    USING_CUSTOM_FONT = False

# === Release any displays that might already be in use ===
displayio.release_displays()

# === Setup I2C display using STEMMA QT ===
i2c = board.STEMMA_I2C()  # Uses default I2C pins for QT Py RP2040
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3D)

WIDTH = 128
HEIGHT = 128

# === Initialize the SSD1327 OLED Display ===
display = adafruit_ssd1327.SSD1327(
    display_bus, width=WIDTH, height=HEIGHT, rotation=0
)

# === Create the main display group ===
main_group = displayio.Group()
display.root_group = main_group

# === Add text labels with unique names ===
# Title at the top
header = label.Label(
    font,
    text="1.5\" 128x128",
    color=0xFFFFFF,
    scale=1,
    x=5,
    y=10,
)
main_group.append(header)

# Pros and cons with proper variable names
pro_label = label.Label(
    font,
    text="+ Easy setup",
    color=0xFFFFFF,
    scale=1,
    x=5,
    y=25,  # Increased spacing for better readability
)
main_group.append(pro_label)

con1_label = label.Label(
    font,
    text="- Slow (I2C)",
    color=0xFFFFFF,
    scale=1,
    x=5,
    y=40,  # Increased spacing
)
main_group.append(con1_label)

con2_label = label.Label(
    font,
    text="- Can't be left",
    color=0xFFFFFF,
    scale=1,
    x=5,
    y=55,  # Increased spacing
)
main_group.append(con2_label)

con3_label = label.Label(
    font,
    text="  on. No color.",
    color=0xFFFFFF,
    scale=1,
    x=5,
    y=70,  # Increased spacing
)
main_group.append(con3_label)

# === Create a 64x64 bitmap and grayscale palette ===
size = 32
bitmap = displayio.Bitmap(size, size, 256)
palette = displayio.Palette(256)
for i in range(256):
    palette[i] = (i << 16) | (i << 8) | i  # Grayscale color ramp

# Position the animation at the bottom of the display
tile = displayio.TileGrid(
    bitmap,
    pixel_shader=palette,
    x=(WIDTH - size) // 2,     # Center horizontally
    y=HEIGHT - size - 5        # Position at bottom with a small 5px margin
)
main_group.append(tile)

# === Function to animate a grayscale pulse ===
def animate_pulse(frame):
    for y in range(size):
        for x in range(size):
            dx = x - size // 2
            dy = y - size // 2
            dist = math.sqrt(dx * dx + dy * dy)
            brightness = int(127 + 127 * math.sin(dist / 3 - frame / 5)) % 256
            bitmap[x, y] = brightness

# === Main loop ===
frame = 0
# Animation speed and framerate control
ANIMATION_SPEED = 2  # Higher = faster animation
FRAME_DELAY = 0.05   # Lower = more CPU usage but potentially smoother

while True:
    animate_pulse(frame)
    frame += ANIMATION_SPEED
    time.sleep(FRAME_DELAY)