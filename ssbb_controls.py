

from keyboard import Keyboard
actionKeys =['left', 'right', 'up', 'down', 'q', 'd', 'w', 'a', 's','z', 'm', 'x', 'z',' ']
directionKeys = ['left', 'right', 'up', 'down']

class Action():
    def __init__(self, key, sustain=False, multi=False, otherKey=None):
        self.key = key
        self.sustain = sustain
        self.multi = multi
        self.otherKey = otherKey

    def params(self):
        return (self.key, self.sustain, self.multi, self.otherKey)


actionCnfg = {
    'hard left':    Action('left', True),
    'hard right':   Action('right', True),
    'left':         Action('left', True, True, 'm'),
    'right':        Action('right', True, True, 'm'),
    'up':           Action('up', True),
    'down':         Action('down', True),
    'block':        Action('q', True),
    'rHand jab':    Action('x', True),
    'rHand right':  Action('d'),
    'rHand up':     Action('w'),
    'rHand left':   Action('a'),
    'rHand down':   Action('s'),
    'lHand jab':    Action('z', True),
    'lHand right':  Action('z', False, True, 'right'),
    'lHand up':     Action('z', False, True, 'up'),
    'lHand left':   Action('z', False, True, 'left'),
    'lHand down':   Action('z', False, True, 'down'),
    'start':        Action(' ')
}






if __name__ == "__main__":
    keyboard = Keyboard()

    for key in actionKeys:
        keyboard.KeyUp(key)