from controls.Action import Action

actionKeys =['left', 'right', 'up', 'down', 'q', 'd', 'w', 'a', 's','z', 'm', 'x', 'z',' ']
directionKeys = ['left', 'right', 'up', 'down']
actionsNames = [
    'left', 'right', 'jump', 'duck', 'block', 'hard left', 'hard right', 'start',
    'rHand jab', 'rHand right', 'rHand up', 'rHand left', 'rHand down',
    'lHand jab', 'lHand right', 'lHand up', 'lHand left', 'lHand down',
    'lHand up_left', 'lHand up_right'
]



actionCnfg = {
    'hard left':    Action('left', False),
    'hard right':   Action('right', False),
    'left':         Action('left', True, True, 'm'),
    'right':        Action('right', True, True, 'm'),
    'jump':           Action('up', True),
    'duck':         Action('down', True),
    'block':        Action('q', True),
    'rHand jab':    Action('x', True),
    'rHand right':  Action('d'),
    'rHand up':     Action('w'),
    'rHand left':   Action('a'),
    'rHand down':   Action('s'),
    'lHand jab':    Action('z', True),
    'lHand right':  Action('z', False, True, 'right'),
    'lHand up':     Action('z', False, True, 'up', delay=.01),
    'lHand left':   Action('z', False, True, 'left'),
    'lHand down':   Action('z', False, True, 'down'),
    'lHand up_left':     Action('z', False, True, 'up', 'left', delay=.01),
    'lHand up_right':     Action('z', False, True, 'up', 'right', delay=.01),
    'start':        Action(' '),
}

