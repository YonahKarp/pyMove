from controls.Action import Action

actionKeys =['left', 'right', 'up', 'down', '1', '2', 'a', 'b', '=', '-', 's', 'c', 'z', 'm']
directionKeys = ['left', 'right', 'up', 'down']
actionsNames = [
    'left', 'right', 'fwd', 'back', 'jump',
    'fire', 'beam', 'visor', 'missle', 
    'lock', 'morph',
    'map', 'pause'
]


# key, sustain, multi, otherKey, keepDirection
actionCnfg = {
    'left':     Action('left', True, True, 'm'),
    'right':    Action('right', True, True, 'm'),
    'fwd':      Action('up', True),
    'back':     Action('down', True),
    'jump':     Action('b', True),

    'fire':     Action('a', True),
    'beam':     Action('=', True),
    'visor':    Action('-', True),
    'missle':   Action('s', True),
    'morph':    Action('c', True),
    'lock':     Action('z', True),

    'map':   Action('1', True),
    'pause':   Action('2', True),
}
