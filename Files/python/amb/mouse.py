from pynput.mouse import Listener
import math
import time
import calendar

# detect mouse move
def on_move(x, y):
    print('Pointer moved to {0}'.format((x, y)))
    f = open('logger.txt', 'a')
    ts = calendar.timegm(time.gmtime())
    f.write(str(ts) + ':' + 'Pointer moved to {0}\n'.format((x, y)))
    f.close()
def on_click(x, y, button, pressed):
    if pressed:
        print('Pointer moved to {0}'.format((x, y)))
        f = open('logger.txt', 'a')
        ts = calendar.timegm(time.gmtime())
        f.write(str(ts) + ':' + 'Mouse Click \n')
        f.close()
# detect mouse scroll
def on_scroll(x, y, dx, dy):
    print('Pointer moved to {0}'.format((x, y)))
    f = open('logger.txt', 'a')
    ts = calendar.timegm(time.gmtime())
    f.write(str(ts) + ':' + 'Mouse Scroll \n')
    f.close()
# Collect events
with Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll) as listener:
    listener.join()



