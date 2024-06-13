from pynput import keyboard


def on_press(key):

    try:
        if key == keyboard.Key.f6:
            print("f6")
        elif key == keyboard.Key.f7:
            print("f7")
    except Exception as e:
        print(f"Ошибка: {e}")

# Запуск слушателя
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()


'''import asyncio
import keyboard


class ControlPanel:
    async def run(self):
        while True:
            if keyboard.is_pressed('f6'):
                print("f6")
                print("word:")
                word = input()
                print(f"{word=}")
                await asyncio.sleep(2)
            if keyboard.is_pressed('f7'):
                print("f7")


if __name__ == '__main__':
    panel = ControlPanel()
    asyncio.run(panel.run())
'''