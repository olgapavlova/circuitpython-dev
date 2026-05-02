import time
import board
import displayio

display = board.DISPLAY
display.brightness = 0.0

# --- утилиты ---

def full_screen(color):
    group = displayio.Group()

    bitmap = displayio.Bitmap(display.width, display.height, 1)
    palette = displayio.Palette(1)
    palette[0] = color

    tile = displayio.TileGrid(bitmap, pixel_shader=palette)
    group.append(tile)

    try:
        display.root_group = group
    except AttributeError:
        display.show(group)


def moving_pixel():
    bitmap = displayio.Bitmap(display.width, display.height, 1)
    palette = displayio.Palette(1)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF

    tile = displayio.TileGrid(bitmap, pixel_shader=palette)
    group = displayio.Group()
    group.append(tile)

    try:
        display.root_group = group
    except AttributeError:
        display.show(group)

    x = 0
    y = display.height // 2

    while True:
        bitmap.fill(0)
        bitmap[x, y] = 1

        x += 1
        if x >= display.width:
            x = 0

        time.sleep(0.01)


def moving_circle(radius=10):
    size = radius * 2 + 1

    bitmap = displayio.Bitmap(size, size, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF

    # рисуем круг в bitmap
    cx = cy = radius
    for x in range(size):
        for y in range(size):
            dx = x - cx
            dy = y - cy
            if dx*dx + dy*dy <= radius*radius:
                bitmap[x, y] = 1

    tile = displayio.TileGrid(bitmap, pixel_shader=palette)
    group = displayio.Group()
    group.append(tile)

    try:
        display.root_group = group
    except AttributeError:
        display.show(group)

    x = 0
    y = display.height // 2 - radius
    dx = 2

    while True:
        tile.x = x
        tile.y = y

        x += dx
        if x <= 0 or x >= display.width - size:
            dx = -dx

        time.sleep(0.02)


# --- запуск тестов ---

# 1. мигание
for _ in range(6):
    full_screen(0xFFFFFF)
    time.sleep(0.3)
    full_screen(0x000000)
    time.sleep(0.3)

# 2. бегущая точка
# moving_pixel()

# 3. движущийся круг
moving_circle()