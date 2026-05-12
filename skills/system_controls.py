import subprocess
import ctypes
from ctypes import cast, POINTER

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
        subprocess.call(["nircmd.exe", "changesysvolume", "6553"])
        return "Volume up!"

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

def media_pause():
    import ctypes
    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)  # VK_MEDIA_PLAY_PAUSE
    return "Paused!"

def media_next():
    ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)  # VK_MEDIA_NEXT_TRACK
    return "Next track!"

def media_prev():
    ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)  # VK_MEDIA_PREV_TRACK
    return "Previous track!"

def shutdown():
    subprocess.run(["shutdown", "/s", "/t", "10"])
    return "Shutting down in 10 seconds!"

def restart():
    subprocess.run(["shutdown", "/r", "/t", "10"])
    return "Restarting in 10 seconds!"

def sleep():
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
    return "Going to sleep!"

def cancel_shutdown():
    subprocess.run(["shutdown", "/a"])
    return "Shutdown cancelled!"

def lock_pc():
    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    return "PC locked!"