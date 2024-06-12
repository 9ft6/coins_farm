import platform
import os


def clear_screen():
    current_os = platform.system()

    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def readable(num):
    num = int(num)
    if num >= 1_000_000_000:
        return f'{num / 1_000_000_000:.3f}b'
    elif num >= 1_000_000:
        return f'{num / 1_000_000:.1f}m'
    elif num >= 1_000:
        return f'{int(num / 1_000)}k'
    else:
        return str(num)
