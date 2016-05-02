import ImageGrab
import os
import time

"""
Coordinates calculated on home PC with game
window on left half of screen
x_pad = 222
y_pad = 351
x_max = 722
y_max = 851

"""

x_pad = 222
y_pad = 351

def screenGrab():
    box = (x_pad, y_pad, 722, 851)
    im = ImageGrab.grab(box)
    #im.save(os.getcwd() + '\\full_snap__' +str(int(time.time())) + '.png', 'PNG')
    return im

def main():
    screenGrab()

if __name__ == '__main__':
    main()
