import platform
import os

from pydantic import BaseModel

from config import cfg


def enable_emoji(s):
    if cfg.use_emoji:
        return "🟢" if s else "🔴"
    else:
        return "(+)" if s else "(-)"


def clear_screen():
    current_os = platform.system()

    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def readable(num):
    num = int(num)

    if abs(num) >= 1_000_000_000:
        result = f'{num / 1_000_000_000:.3f}b'
    elif abs(num) >= 1_000_000:
        result = f'{num / 1_000_000:.1f}m'
    elif abs(num) >= 1_000:
        result = f'{int(num / 1_000)}k'
    else:
        result = str(num)

    if result.startswith('-'):
        result = result.replace("-", "- ")

    return result


def jsonify(v):
    if isinstance(v, BaseModel):
        return v.model_dump()
    if isinstance(v, dict):
        return {k: jsonify(v) for k, v in v.items()}
    if isinstance(v, list | tuple | set):
        return type(v)([jsonify(v) for v in v])
    else:
        return v
