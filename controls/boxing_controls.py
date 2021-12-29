from Keyboard import keyboard
from controls.Action import Action

actionKeys =['left', 'right', 'up', 'down', 'w', 'a', 's', 'd', 'x', 'z']
directionKeys = ['left', 'right', 'a','d']
actionsNames = [
    'left', 'right', 'block',
    'rjab', 'rhook', 
    'ljab', 'lhook',
    'press a'
]


# key, sustain, multi, otherKey, keepDirection
actionCnfg = {
    'left':         Action('left', True, True, 'a'),
    'right':        Action('right', True, True, 'd'),
    'block':           Action('left', True, True, 'd'),
    'rhook':    Action('right', True, True, 'down'),
    'lhook':    Action('left', True, True, 's'),
    'rjab':     Action('w', True),
    'ljab':  Action('up', True),
    'press a':   Action('x'),
    'press ab': Action('x', False, True, 'z')
}

if __name__ == "__main__":
    for key in actionKeys:
        keyboard.KeyUp(key)