import time
import pynput.keyboard as Keyboard
from datetime import datetime
import BetterPrinting as bp

data = []

def on_press(key):
    global start
    # Callback function whenever a key is pressed
    try:
        print(f'Key {key.char} pressed!')
    except AttributeError:
        if key == Keyboard.Key.backspace:
            dt = datetime.now()
            get_time = str(dt).split(":")

            hour, minutes, sec = int(get_time[0][::-1][0:2][::-1]), int(get_time[1]), float(get_time[2])

            all = hour * 3600 + minutes * 60 + sec
            if not data:
                data.append(all)
            minus = all - data[0]
            if minus > 0.05:
                bp.color("geschafft", "green")

            data[0] = all
            print(data)
        print(f'Special Key {key} pressed!')


def on_release(key):
    if key == Keyboard.Key.esc:
        return False


with Keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
