import ctypes
from ctypes import wintypes
import winreg

# Définir les constantes
SPI_GETMOUSE = 0x0003
SPI_GETMOUSETRAILS = 0x005E

# Définir la structure pour les paramètres de la souris
class MouseInfo(ctypes.Structure):
    _fields_ = [("iMouseThreshold1", wintypes.UINT),  # MouseThreshold1
                ("iMouseThreshold2", wintypes.UINT),  # MouseThreshold2
                ("iMouseSpeed", wintypes.UINT)]  # MouseSpeed

def get_mouse_settings_from_api():
    mouse_info = MouseInfo()
    mouse_trails = ctypes.c_int()

    # Obtenir les paramètres de la souris (vitesse et seuils)
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_GETMOUSE, 0, ctypes.byref(mouse_info), 0
    )

    # Obtenir la longueur des traînées du curseur
    result_trails = ctypes.windll.user32.SystemParametersInfoW(
        SPI_GETMOUSETRAILS, 0, ctypes.byref(mouse_trails), 0
    )

    if result and result_trails:
        return {
            "MouseSpeed": mouse_info.iMouseSpeed,
            "MouseThreshold1": mouse_info.iMouseThreshold1,
            "MouseThreshold2": mouse_info.iMouseThreshold2,
            "MouseTrails": mouse_trails.value
        }
    else:
        raise RuntimeError("Failed to get mouse settings from API")

def get_mouse_settings_from_registry():
    settings = {}
    registry_path = r"Control Panel\Mouse"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path) as key:
            settings["MouseSpeed"] = int(winreg.QueryValueEx(key, "MouseSpeed")[0])
            settings["MouseThreshold1"] = int(winreg.QueryValueEx(key, "MouseThreshold1")[0])
            settings["MouseThreshold2"] = int(winreg.QueryValueEx(key, "MouseThreshold2")[0])
            settings["MouseTrails"] = int(winreg.QueryValueEx(key, "MouseTrails")[0])
    except FileNotFoundError as e:
        raise RuntimeError(f"Failed to get mouse settings from registry: {e}")

    return settings

# Utilisation de la fonction
settings_api = get_mouse_settings_from_api()
settings_registry = get_mouse_settings_from_registry()

print("Paramètres de la souris depuis l'API :")
print(settings_api)

print("Paramètres de la souris depuis le Registre :")
print(settings_registry)
