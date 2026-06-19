import subprocess
import ctypes
from ctypes import cast, POINTER
import datetime

# =========================
# VOLUME CONTROLS
# =========================

def volume_up():
    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(1.0, current + 0.1), None)
        return "Volume up!"
    except:
        return "Couldn't change volume!"

def volume_down():
    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(max(0.0, current - 0.1), None)
        return "Volume down!"
    except:
        return "Couldn't change volume!"

def mute():
    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)
        return "Muted!"
    except:
        return "Couldn't mute!"

def unmute():
    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)
        return "Unmuted!"
    except:
        return "Couldn't unmute!"

def get_volume_level():
    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        return f"Volume is at {int(current * 100)}%"
    except:
        return "Couldn't check volume!"

def set_volume(percent):
    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(percent / 100, None)
        return f"Volume set to {percent}%!"
    except:
        return "Couldn't set volume!"

# =========================
# MEDIA CONTROLS
# =========================

def media_pause():
    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
    return "Paused!"

def media_next():
    ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)
    return "Next track!"

def media_prev():
    ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)
    return "Previous track!"

def media_stop():
    ctypes.windll.user32.keybd_event(0xB2, 0, 0, 0)
    return "Stopped!"

# =========================
# BRIGHTNESS
# =========================

def get_brightness():
    try:
        import screen_brightness_control as sbc
        brightness = sbc.get_brightness()[0]
        return f"Screen brightness is at {brightness}%"
    except:
        return "Couldn't check brightness!"

def set_brightness(level):
    try:
        import screen_brightness_control as sbc
        sbc.set_brightness(level)
        return f"Brightness set to {level}%!"
    except:
        return "Couldn't set brightness!"

def brightness_up():
    try:
        import screen_brightness_control as sbc
        current = sbc.get_brightness()[0]
        new_level = min(100, current + 10)
        sbc.set_brightness(new_level)
        return f"Brightness increased to {new_level}%!"
    except:
        return "Couldn't change brightness!"

def brightness_down():
    try:
        import screen_brightness_control as sbc
        current = sbc.get_brightness()[0]
        new_level = max(0, current - 10)
        sbc.set_brightness(new_level)
        return f"Brightness decreased to {new_level}%!"
    except:
        return "Couldn't change brightness!"

# =========================
# POWER CONTROLS
# =========================

def shutdown():
    subprocess.run(["shutdown", "/s", "/t", "10"])
    return "Shutting down in 10 seconds!"

def restart():
    subprocess.run(["shutdown", "/r", "/t", "10"])
    return "Restarting in 10 seconds!"

def sleep():
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
    return "Going to sleep!"

def hibernate():
    subprocess.run(["shutdown", "/h"])
    return "Hibernating!"

def log_off():
    subprocess.run(["shutdown", "/l"])
    return "Logging off!"

def cancel_shutdown():
    subprocess.run(["shutdown", "/a"])
    return "Shutdown cancelled!"

def lock_pc():
    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    return "PC locked!"

def unlock_pc():
    return "I can't actually unlock it for security reasons — you'll need to enter your PIN or password!"

# =========================
# UTILITY
# =========================

def open_task_manager():
    subprocess.Popen("taskmgr.exe")
    return "Opening task manager!"

def empty_recycle_bin():
    try:
        import winshell
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        return "Recycle bin emptied!"
    except Exception as e:
        return f"Couldn't empty recycle bin: {e}"

def take_screenshot_quick():
    try:
        import pyautogui
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(filename)
        return f"Screenshot saved as {filename}!"
    except Exception as e:
        return f"Couldn't take screenshot: {e}"

def open_control_panel():
    subprocess.Popen("control.exe")
    return "Opening control panel!"

def open_settings():
    subprocess.Popen("start ms-settings:", shell=True)
    return "Opening settings!"

def eject_disk():
    try:
        subprocess.run(["powershell", "-command", "(New-Object -comObject Shell.Application).Namespace(17).ParseName('D:').InvokeVerb('Eject')"])
        return "Disk ejected!"
    except:
        return "Couldn't eject disk!"

def toggle_wifi(state="on"):
    try:
        if state == "on":
            subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enabled"])
            return "WiFi turned on!"
        else:
            subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "disabled"])
            return "WiFi turned off!"
    except:
        return "Couldn't toggle WiFi!"

def open_file_explorer():
    subprocess.Popen("explorer.exe")
    return "Opening file explorer!"

def minimize_all_windows():
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Win key
    ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)  # D key
    return "Minimized all windows!"