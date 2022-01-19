""" This module provides tools for programmatic control of the Dolphin emulator via fifo pipes.
Note: More information about the Dolphin emulator can be found at:
    https://dolphin-emu.org/
    https://github.com/dolphin-emu/dolphin
"""

import enum
import os
import time
from threading import Timer


@enum.unique
class Button(enum.Enum):
    """ Supported Dolphin buttons """
    A = 0
    B = 1
    X = 2
    Y = 3
    Z = 4
    START = 5
    L = 6
    R = 7
    D_UP = 8
    D_DOWN = 9
    D_LEFT = 10
    D_RIGHT = 11


@enum.unique
class Trigger(enum.Enum):
    """ Supported Dolphin triggers """
    L = 0
    R = 1


@enum.unique
class Stick(enum.Enum):
    """ Supported Dolphin  sticks """
    MAIN = 0
    C = 1


class DolphinControls:

    def __init__(self, path):

        controls = [*Button, *Stick]

        self.isSet = dict(zip(controls, [False]*len(controls)))

        self.pipe = None
        self.path = os.path.expanduser(path)
        # self.path = path

    def __enter__(self):
        """ Open the fifo pipe. Blocks until the other side is listening. """
        print('opening pipe')
        self.pipe = open(self.path, 'w', buffering=1)
        print('pipe opened')
        return self

    def __exit__(self, *args):
        """ Close the fifo pipe. """
        if self.pipe:
            self.pipe.close()

    def press_button(self, button):
        assert button in Button
        self.isSet[button] = True
        self.pipe.write('PRESS {}\n'.format(button.name))
        

    def release_button(self, button):
        assert button in Button
        if(self.isSet[button]):
            self.isSet[button] = False
            self.pipe.write('RELEASE {}\n'.format(button.name))


    def set_trigger(self, trigger, amount):
        assert trigger in Trigger
        assert 0 <= amount <= 1
        self.pipe.write('SET {} {:.2f}\n'.format(trigger.name, amount))

    def set_stick(self, stick, x, y):
        assert stick in Stick
        assert 0 <= x <= 1 and 0 <= y <= 1
        self.isSet[stick] = True
        self.pipe.write('SET {} {:.2f} {:.2f}\n'.format(stick.name, x, y))


    def reset_stick(self, stick):
        if(self.isSet[stick]):
            self.isSet[stick] = False
            self.pipe.write('SET {} {:.2f} {:.2f}\n'.format(stick.name, .5, .5))


    def reset(self):
        """ Reset all Dolphin controller elements to released or neutral position. """
        for button in Button:
            self.release_button(button)
            self.isSet[button] = False
        for trigger in Trigger:
            self.set_trigger(trigger, 0)
        for stick in Stick:
            self.reset_stick(stick)
            self.isSet[stick] = False


        

path = '/Users/yonahkarp/Library/Application Support/Dolphin/Pipes/pipe1'
dolphinControls = DolphinControls(path).__enter__()