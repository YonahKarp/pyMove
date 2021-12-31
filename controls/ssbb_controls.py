from controls.Action import Action

actionKeys =['left', 'right', 'up', 'down', 'q', 'd', 'w', 'a', 's','z', 'm', 'x', 'y', 'z',' ']
directionKeys = ['left', 'right', 'up', 'down']
actionsNames = [
    'left', 'right', 'jump', 'duck', 'up', 'block', 'hard left', 'hard right', 'start',
    'rHand jab', 'rHand right', 'rHand up', 'rHand left', 'rHand down', 'rHand uptilt',
    'lHand jab', 'lHand right', 'lHand up', 'lHand left', 'lHand down', 
    'lHand up_left', 'lHand up_right'
]



actionCnfg = {
    'hard left':    Action('left', False),
    'hard right':   Action('right', False),
    'left':         Action('left', True, True, 'm'),
    'right':        Action('right', True, True, 'm'),
    'jump':           Action('y', True),
    'up':           Action('up', True),
    'duck':         Action('down', True),
    'block':        Action('q', True),
    'rHand jab':    Action('x', True),
    'rHand right':  Action('d'),
    'rHand up':     Action('w'),
    'rHand uptilt': Action('x', False, delay=.08), #in combination with sustain up and no tap jump
    'rHand left':   Action('a'),
    'rHand down':   Action('s'),
    'lHand jab':    Action('z', True),
    'lHand up':     Action('z', False, True, 'up', delay=.01),
    'lHand left':   Action('z', False, True, 'left'),
    'lHand right':  Action('z', False, True, 'right'),
    'lHand down':   Action('z', False, True, 'down'),
    'lHand up_left':     Action('z', False, True, 'up', 'left', delay=.01),
    'lHand up_right':     Action('z', False, True, 'up', 'right', delay=.01),
    'start':        Action(' '),
}

