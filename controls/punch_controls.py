from controls.Action import Action

actionKeys =['left', 'right', 'up', 'down', '1', '2', 'x']
directionKeys = ['left', 'right', 'up', 'down']
actionsNames = [
    'left', 'right', 'block', 'duck',
    'rjab', 'rhook', 
    'ljab', 'lhook',
    'star punch'
]


# key, sustain, multi, otherKey, keepDirection
actionCnfg = {
    'left':         Action('up', True),
    'right':        Action('down', True),
    'block':           Action('right', True),
    'duck':         Action('left', True),
    'rhook':    Action('2', True),
    'lhook':    Action('1', True),
    'rjab':     Action('2', True, True, 'right'),
    'ljab':  Action('1', True, True, 'right'),
    'star punch':   Action('x'),
}