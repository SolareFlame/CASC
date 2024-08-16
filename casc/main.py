import time
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image
from plyer import notification

from casc.detect import detect_app, load_app
from casc.edit import set_mouse_settings_to_zero, reset_mouse_settings

ICON_PATHS = {
    "enabled": "res/enabled.png",
    "disabled": "res/disabled.png",
    "nodetect": "res/nodetect.png"
}

detect_enabled = True

def update_icon():
    if not detect_enabled:
        icon.icon = Image.open(ICON_PATHS["nodetect"])
    elif detect_app()[0]:
        icon.icon = Image.open(ICON_PATHS["disabled"])
    else:
        icon.icon = Image.open(ICON_PATHS["enabled"])


def create_menu():
    return Menu(
        MenuItem("Disable Detection" if detect_enabled else "Enable Detection", toggle_detection, default=True),
        MenuItem("Quit", on_quit)
    )


def toggle_detection(icon, item):
    global detect_enabled
    detect_enabled = not detect_enabled

    if not detect_enabled:
        reset_mouse_settings()

    update_icon()
    icon.menu = create_menu()


def notify_user(message):
    notification.notify(
        title="Mouse Threshold Control",
        message=message,
        timeout=5
    )


def start_detection():
    activated = False

    while True:
        if detect_enabled:
            detected, process_name = detect_app()
            if detected:
                set_mouse_settings_to_zero()

                if not activated:
                    notify_user(f"{process_name} detected")

                activated = True
            else:
                reset_mouse_settings()
                activated = False
        time.sleep(5)
        update_icon()


def on_quit(icon, item):
    global detect_enabled
    detect_enabled = False
    icon.stop()


def setup_tray_icon():
    load_app("config.json")

    global icon
    icon = Icon("MTHc")
    icon.title = "Mouse Threshold Control"

    update_icon()
    icon.menu = create_menu()

    icon.run()


if __name__ == "__main__":
    detection_thread = Thread(target=start_detection)
    detection_thread.daemon = True
    detection_thread.start()

    setup_tray_icon()
