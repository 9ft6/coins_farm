import platform
import os

from config import cfg


def clear_screen():
    current_os = platform.system()

    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')
