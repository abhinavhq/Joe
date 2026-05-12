import psutil
import platform


def get_system_info():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_used = ram.percent
    ram_total = round(ram.total / (1024 ** 3), 1)
    battery = psutil.sensors_battery()

    info = f"CPU is at {cpu}%, RAM usage is {ram_used}% out of {ram_total} GB"

    if battery:
        bat = round(battery.percent)
        charging = "and charging" if battery.power_plugged else "not charging"
        info += f", battery is at {bat}% {charging}"

    return info


def get_battery():
    battery = psutil.sensors_battery()
    if battery:
        bat = round(battery.percent)
        charging = "and charging" if battery.power_plugged else "not charging"
        return f"Battery is at {bat}% {charging}!"
    return "Couldn't get battery info!"


def get_cpu():
    cpu = psutil.cpu_percent(interval=1)
    return f"CPU usage is {cpu}%"


def get_ram():
    ram = psutil.virtual_memory()
    return f"RAM usage is {ram.percent}%, {round(ram.available / (1024 ** 3), 1)}GB available"


def get_disk():
    disk = psutil.disk_usage('/')
    return f"Disk usage is {disk.percent}%, {round(disk.free / (1024 ** 3), 1)}GB free"