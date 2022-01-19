from controls.Action import Action
from DolphinControls import Button


actionKeys =[Button.D_UP, Button.D_DOWN, Button.D_LEFT, Button.D_RIGHT, Button.X, Button.Y, Button.A]
directionKeys = ['left', 'right', 'up', 'down']
actionsNames = [
    'left', 'right', 'block', 'duck',
    'rjab', 'rhook', 
    'ljab', 'lhook',
    'star punch'
]


# key, sustain, multi, otherKey, keepDirection
actionCnfg = {
    'left':         Action(Button.D_UP, True),
    'right':        Action(Button.D_DOWN, True),
    'block':           Action(Button.D_RIGHT, True),
    'duck':         Action(Button.D_LEFT, True),
    'rhook':    Action(Button.Y, True),
    'lhook':    Action(Button.X, True),
    'rjab':     Action(Button.Y, True, True, Button.D_RIGHT),
    'ljab':  Action(Button.X, True, True, Button.D_RIGHT),
    'star punch':   Action(Button.A),
}