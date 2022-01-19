from controls.Action import Action
from DolphinControls import Stick, Button

actionKeys =[Stick.MAIN, Stick.C, Button.L, Button.Y, Button.A, Button.B,]
directionKeys = [Stick.MAIN, Stick.C]
actionsNames = [
    'left', 'right', 'jump', 'duck', 'up', 'block', 
    #  'hard left', 'hard right', 
    'rHand jab', 'rHand right', 'rHand up', 'rHand left', 'rHand down', 'rHand uptilt',
    'lHand jab', 'lHand right', 'lHand up', 'lHand left', 'lHand down', 
    # 'lHand up_left', 'lHand up_right', 'start',
]



actionCnfg = {
    # 'hard left':    Action('left', False),
    # 'hard right':   Action('right', False),
    'left':         Action(Stick.MAIN, True, isStick=True),
    'right':        Action(Stick.MAIN, True, isStick=True),
    'jump':           Action(Button.Y, True),
    'up':           Action(Stick.MAIN, True, isStick=True),
    'duck':         Action(Stick.MAIN, True, isStick=True),
    'block':        Action(Button.L, True),
    'rHand jab':    Action(Button.A, True),
    'rHand right':  Action(Stick.C, isStick=True),
    'rHand up':     Action(Stick.C, isStick=True),
    'rHand uptilt': Action(Button.A, False, delay=.08), #in combination with sustain up and no tap jump
    'rHand left':   Action(Stick.C, isStick=True),
    'rHand down':   Action(Stick.C, isStick=True),
    'lHand jab':    Action(Button.B, True),
    'lHand up':     Action(Stick.MAIN, False, True, Button.B, isStick=True),
    'lHand left':   Action(Stick.MAIN, False, True, Button.B, isStick=True),
    'lHand right':  Action(Stick.MAIN, False, True, Button.B, isStick=True),
    'lHand down':   Action(Stick.MAIN, False, True, Button.B, isStick=True),
    # 'lHand up_left':     Action(Stick.MAIN, False, True, 'B', 'left', delay=.01),
    # 'lHand up_right':     Action(Stick.MAIN, False, True, 'B', 'right', delay=.01),
    # 'start':        Action(Button.START)
}

