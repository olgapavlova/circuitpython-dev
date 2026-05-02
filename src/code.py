import os
import time
import json
import storage
import sdioio
import digitalio

from adafruit_ble import BLERadio

SCAN_SECONDS = 30
MIN_RSSI = -120
SD_MOUNT = "/sd"
OUT_DIR = "/sd/ble_adv"

# Если авто-поиск не найдёт пины, сюда надо вписать реальные:
# SD_SCK = board.IO...
# SD_MOSI = board.IO...
# SD_MISO = board.IO...
# SD_CS = board.IO...

PIN_CANDIDATES = {
    "sck":  ["SD_SCK", "SDCARD_SCK", "SCK", "IO12"],
    "mosi": ["SD_MOSI", "SDCARD_MOSI", "MOSI", "IO11"],
    "miso": ["SD_MISO", "SDCARD_MISO", "MISO", "IO13"],
    "cs":   ["SD_CS", "SDCARD_CS", "CS", "IO10"],
}

import board
import displayio
import terminalio
from adafruit_display_text import label

DISPLAY_UPDATE_SECONDS = 60

display = board.DISPLAY

screen = displayio.Group()
bg_bitmap = displayio.Bitmap(display.width, display.height, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x000000
bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
screen.append(bg)

status_label = label.Label(
    terminalio.FONT,
    text="SD usage...",
    color=0xFFFFFF,
    background_color=0x000000,
    scale=2,
    x=4,
    y=18,
)

screen.append(status_label)

try:
    display.root_group = screen
except AttributeError:
    display.show(screen)

def find_pin(names):
    for name in names:
        if hasattr(board, name):
            return getattr(board, name), name
    return None, None


def mount_sd():
    print("Mounting SD via SDIO")

    sd = sdioio.SDCard(
        clock=board.SD_SCK,
        command=board.SD_CMD,
        data=[
            board.SD_D0,
            board.SD_D1,
            board.SD_D2,
            board.SD_D3,
        ],
        frequency=25000000,
    )

    vfs = storage.VfsFat(sd)
    storage.mount(vfs, SD_MOUNT)

    try:
        os.mkdir(OUT_DIR)
    except OSError:
        pass

    print("SD mounted:", SD_MOUNT)

def json_safe(value):
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, bytes):
        return {
            "hex": " ".join("{:02X}".format(b) for b in value),
            "len": len(value),
        }

    if isinstance(value, (list, tuple)):
        return [json_safe(x) for x in value]

    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            out[str(k)] = json_safe(v)
        return out

    return str(value)

def adv_to_dict(adv):
    data = {
        "time_monotonic": time.monotonic(),
        "address": str(adv.address),
        "rssi": adv.rssi,
        "advertisement_type": type(adv).__name__,
        "connectable": json_safe(getattr(adv, "connectable", None)),
        "scan_response": json_safe(getattr(adv, "scan_response", None)),
        "complete_name": json_safe(getattr(adv, "complete_name", None)),
        "short_name": json_safe(getattr(adv, "short_name", None)),
        "tx_power": json_safe(getattr(adv, "tx_power", None)),
        "appearance": json_safe(getattr(adv, "appearance", None)),
        "service_uuids": json_safe(getattr(adv, "service_uuids", None)),
        "service_data": json_safe(getattr(adv, "service_data", None)),
        "manufacturer_data": json_safe(getattr(adv, "manufacturer_data", None)),
        "public_attrs": {},
    }

    for name in sorted(dir(adv)):
        if name.startswith("_"):
            continue

        try:
            value = getattr(adv, name)
        except Exception as e:
            value = "ERROR: {}".format(e)

        if callable(value):
            continue

        data["public_attrs"][name] = json_safe(value)

    return data

def safe_filename_part(text):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    return "".join(c if c in allowed else "_" for c in str(text))

def make_filename(adv):
    ms = int(time.monotonic() * 1000)
    addr = safe_filename_part(adv.address)
    return "{}/ble_{}_{}.json".format(OUT_DIR, ms, addr)

def write_adv_json(adv):
    path = make_filename(adv)
    data = adv_to_dict(adv)

    with open(path, "w") as f:
        json.dump(data, f)

    print("saved:", path)

def bytes_to_mb(value):
    return value / 1024 / 1024

def fs_usage_text(path):
    s = os.statvfs(path)

    block_size = s[0]
    total_blocks = s[2]
    free_blocks = s[3]

    total = block_size * total_blocks
    free = block_size * free_blocks
    used = total - free

    return "used: {:4.0f} MB\nfree: {:4.0f} MB".format(
        bytes_to_mb(used),
        bytes_to_mb(free),
    )

def update_display_usage():
    try:
        status_label.text = fs_usage_text(SD_MOUNT)
    except Exception as e:
        status_label.text = "SD error\n{}".format(e)

print("BLE advertising logger to SD")
mount_sd()

ble = BLERadio()

last_display_update = 0
update_display_usage()

while True:
    now = time.monotonic()

    if now - last_display_update >= DISPLAY_UPDATE_SECONDS:
        update_display_usage()
        last_display_update = now

    print("Scanning...")

    for adv in ble.start_scan(timeout=SCAN_SECONDS):
        if adv.rssi < MIN_RSSI:
            continue

        try:
            write_adv_json(adv)
        except Exception as e:
            print("write failed:", e)

    ble.stop_scan()
    time.sleep(1)