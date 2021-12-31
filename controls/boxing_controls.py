from controls.Action import Action

actionKeys =['left', 'right', 'up', 'down', 'w', 'a', 's', 'd', 'x', 'z']
directionKeys = ['left', 'right', 'a','d']
actionsNames = [
    'left', 'right', 'block',
    'rjab', 'rhook', 
    'ljab', 'lhook',
    'press a', 'press ab'
]


# key, sustain, multi, otherKey, keepDirection
actionCnfg = {
    'left':     Action('left', True, True, 'a'),
    'right':    Action('right', True, True, 'd'),
    'block':    Action('left', True, True, 'd'),
    'rhook':    Action('up', True),
    'lhook':    Action('w', True),
    'rjab':     Action('down', True),
    'ljab':     Action('s', True),
    'press a':  Action('x'),
    'press ab': Action('x', False, True, 'z')
}