# pip install autodroid
# version: 3.0
# made by: turkishpython
# do not edit db link if you dont have ur own site that gives scrcpy and adb

import os
import requests
import zipfile
import subprocess
from datetime import datetime

db = "https://turkish-db.vercel.app/"
files = {
    "scrcpy": "scrcpy.zip",
    "platform": "platform.zip"
}

for name, zip_name in files.items():
    if not os.path.exists(zip_name.replace(".zip", "")):
        print(f"{name} Doesn't exist, installing...")
        r = requests.get(db + zip_name)
        with open(zip_name, "wb") as f:
            f.write(r.content)
        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            zip_ref.extractall()
        os.remove(zip_name)
        print(f"{name} installed and cleaned up!")

def get_connected_devices():
    result = subprocess.run("platform\\adb devices", shell=True, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:]
    devices = []
    for line in lines:
        if line.strip():
            device_id, status = line.split()
            if status == "device":
                devices.append(device_id)
    return devices

def scrcpy(device=None):
    devices = [device] if device else get_connected_devices()
    for dev in devices:
        subprocess.Popen([f"scrcpy\\scrcpy.exe", "--no-control", "-s", dev])

def tap(x, y, device=None):
    devices = [device] if device else get_connected_devices()
    for dev in devices:
        subprocess.run(f"platform\\adb.exe -s {dev} shell input tap {int(x)} {int(y)}", shell=True)

def swipe(x1, y1, x2, y2, duration, device=None):
    devices = [device] if device else get_connected_devices()
    for dev in devices:
        subprocess.run(f"platform\\adb.exe -s {dev} shell input swipe {int(x1)} {int(y1)} {int(x2)} {int(y2)} {int(duration)}", shell=True)

def type(text, device=None):
    string = str(text).replace(" ", "%s")
    devices = [device] if device else get_connected_devices()
    for dev in devices:
        subprocess.run(f'platform\\adb.exe -s {dev} shell input text "{string}"', shell=True)

def key(key_name, device=None):
    key_map = {
        "home": 3, "back": 4, "recent": 187, "recents": 187, "pwr": 26, "power": 26,
        "v_up": 24, "vol_up": 24, "v_down": 25, "vol_down": 25, "mute": 164,
        "mplay": 85, "play": 85, "wake": 224, "wakeup": 224
    }
    devices = [device] if device else get_connected_devices()
    code = key_map.get(key_name.lower())
    if code:
        for dev in devices:
            subprocess.run(f"platform\\adb.exe -s {dev} shell input keyevent {code}", shell=True)

def holdtap(x, y, dur, device=None):
    devices = [device] if device else get_connected_devices()
    for dev in devices:
        subprocess.run(f"platform\\adb.exe -s {dev} shell input swipe {int(x)} {int(y)} {int(x)} {int(y)} {int(dur)}", shell=True)

def screenshot(device=None):
    today = datetime.now()
    date = today.strftime("%d%m%y")
    time = today.strftime("%H%M%S")
    devices = [device] if device else get_connected_devices()
    for dev in devices:
        autodroidfolder = subprocess.run(f'platform\\adb.exe -s {dev} shell ls /sdcard/autodroid', shell=True, capture_output=True, text=True)
        scFolder = subprocess.run(f'platform\\adb.exe -s {dev} shell ls /sdcard/autodroid/screencap', shell=True, capture_output=True, text=True)

        if "No such file or directory" in autodroidfolder.stdout or "No such file or directory" in autodroidfolder.stderr:
            subprocess.run(f"platform\\adb.exe -s {dev} shell mkdir -p /sdcard/autodroid", shell=True)
        if "No such file or directory" in scFolder.stdout or "No such file or directory" in scFolder.stderr:
            subprocess.run(f"platform\\adb.exe -s {dev} shell mkdir -p /sdcard/autodroid/screencap", shell=True)

        subprocess.run(f"platform\\adb.exe -s {dev} shell screencap -p /sdcard/autodroid/screencap/image_{date}_{time}.png", shell=True)
        subprocess.run(f"platform\\adb.exe -s {dev} pull /sdcard/autodroid/screencap/image_{date}_{time}.png", shell=True)