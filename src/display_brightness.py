import board
import displayio
import time

display = board.DISPLAY

for b in (0.0, 0.25, 0.5, 0.75, 1.0):
    print("brightness", b)
    try:
        display.brightness = b
    except Exception as e:
        print("brightness error:", e)

    group = displayio.Group()
    bitmap = displayio.Bitmap(display.width, display.height, 1)
    palette = displayio.Palette(1)
    palette[0] = 0xFFFFFF
    group.append(displayio.TileGrid(bitmap, pixel_shader=palette))

    try:
        display.root_group = group
    except AttributeError:
        display.show(group)

    time.sleep(2)