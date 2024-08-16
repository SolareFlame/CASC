import psutil
import json

from edit import set_mouse_settings_to_zero, reset_mouse_settings

APPS = []

def detect_app():
    detected = False
    last_process_name = None

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_name = proc.info['name']
            for app in APPS:
                if process_name.lower() == app["process_name"].lower():
                    print(f"MTHc: {app['app_name']} detected")
                    detected = True


                    if app["mouse_threshold"] == 0:
                        print("MTHc: Setting mouse settings to 0 (0)")
                        set_mouse_settings_to_zero()
                    else:
                        print("MTHc: Resetting mouse settings (app disabled) (1)")
                        reset_mouse_settings()
                    last_process_name = process_name
                    break
            if detected:
                break
        except psutil.NoSuchProcess:
            print("MTHc: Process not found")
            continue
        except (psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return detected, last_process_name


def load_app(config_file):
    global APPS
    try:
        with open(config_file, 'r') as file:
            config_data = json.load(file)
            APPS = config_data

            print("MTHc: Configuration loaded successfully.")

            print("Config:" + str(APPS))

    except FileNotFoundError:
        print(f"MTHc: Configuration file '{config_file}' not found.")
    except json.JSONDecodeError:
        print("MTHc: Error decoding JSON from the configuration file.")
    except Exception as e:
        print(f"MTHc: An unexpected error occurred: {e}")

