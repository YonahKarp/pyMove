

from keyboard import Keyboard
actionKeys =['left', 'right', 'up', 'down', 'q', 'd', 'w', 'a', 's','z', 'm']

actionCnfg = {
    'hard left': {
        'key': 'left',
        'type': 'sustain',
    },
    'hard right': {
        'key': 'right',
        'type': 'sustain',
    },
    'm': {
        'key': 'm',
        'type': 'None'
    },
    'left': {
        'key': 'left',
        'otherKey': 'm',
        'otherAction': 'left',
        'type': 'multi',
    },
    'right': {
        'key': 'right',
        'otherKey': 'm',
        'otherAction': 'right',
        'type': 'multi',
    },
    'up': {
        'key': 'up',
        'type': 'sustain',
    },
    'down': {
        'key': 'down',
        'type': 'sustain',
    },
    'block': {
        'key': 'q',
        'type': 'sustain',
    },
    'rHand jab': {
        'key': 'x',
        'type': 'press',
    },
    'rHand right': {
        'key': 'd',
        'type': 'press',
    },
    'rHand up': {
        'key': 'w',
        'type': 'press',
    },
    'rHand left': {
        'key': 'a',
        'type': 'press',
    },
    'rHand down': {
        'key': 's',
        'type': 'press',
    },
    'lHand jab': {
        'key': 'z',
        'type': 'press',
    },
    'lHand right': {
        'key': 'z',
        'otherKey': 'right',
        'otherAction': 'right',
        'type': 'multi',
    }, 
    'lHand up': {
        'key': 'z',
        'otherKey': 'up',
        'otherAction': 'up',
        'type': 'multi',
    },
    'lHand left': {
        'key': 'z',
        'otherKey': 'left',
        'otherAction': 'left',
        'type': 'multi',
    },
    'lHand down': {
        'key': 'z',
        'otherKey': 'down',
        'otherAction': 'down',
        'type': 'multi',
    },
    'start': {
        'key': ' ',
        'type': 'press',
    }
}






if __name__ == "__main__":
    keyboard = Keyboard()

    for key in actionKeys:
        keyboard.KeyUp(key)