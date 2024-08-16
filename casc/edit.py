import ctypes
from ctypes import wintypes

SPI_GETMOUSE = 0x0003
SPI_GETMOUSETRAILS = 0x005E
SPI_SETMOUSE = 0x0004
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

def get_mouse_settings():
    class MouseInfo(ctypes.Structure):
        _fields_ = [
            ("iMouseThreshold1", wintypes.UINT),
            ("iMouseThreshold2", wintypes.UINT),
            ("iXMouse", wintypes.UINT)
        ]

    mouse_info = MouseInfo()

    return {
        "MouseSpeed": mouse_info.iXMouse,
        "MouseThreshold1": mouse_info.iMouseThreshold1,
        "MouseThreshold2": mouse_info.iMouseThreshold2,
    }

def set_mouse_settings_to_zero():
    current_settings = get_mouse_settings()
    if (current_settings["MouseSpeed"] == 0 and
        current_settings["MouseThreshold1"] == 0 and
        current_settings["MouseThreshold2"] == 0):
        print("Mouse settings are already set to zero, no changes needed.")
        return

    params = (ctypes.wintypes.UINT * 3)(0, 0, 0)
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETMOUSE,
        0,
        ctypes.byref(params),
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

    if not result:
        raise RuntimeError("Failed to set mouse settings to 0")
    else:
        print("Mouse settings successfully set to zero.")


def reset_mouse_settings():
    current_settings = get_mouse_settings()
    if (current_settings["MouseSpeed"] == 1 and
        current_settings["MouseThreshold1"] == 6 and
        current_settings["MouseThreshold2"] == 10):
        print("Mouse settings are already set to default, no changes needed.")
        return

    params = (ctypes.wintypes.UINT * 3)(6, 10, 1)
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETMOUSE,
        len(params),
        ctypes.byref(params),
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

    if not result:
        raise RuntimeError("Failed to reset mouse settings to default")
    else:
        print("Mouse settings successfully reset to default.")


print(get_mouse_settings())


