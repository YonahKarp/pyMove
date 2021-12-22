



actionCnfg = {
    'left': {
        'key': 'left',
        'type': 'sustain',
    },
    'right': {
        'key': 'right',
        'type': 'sustain',
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
    'lHand right': {
        'key': 'z',
        'other': 'right',
        'type': 'multi',
    }, 
    'lHand up': {
        'key': 'z',
        'other': 'up',
        'type': 'multi',
    },
    'lHand left': {
        'key': 'z',
        'other': 'left',
        'type': 'multi',
    },
    'lHand down': {
        'key': 'z',
        'other': 'down',
        'type': 'multi',
    }
}



from keyboard import Keyboard
actionKeys =['left', 'right', 'up', 'down', 'q', 'd', 'w', 'a', 's','z']


if __name__ == "__main__":
    keyboard = Keyboard()

    for key in actionKeys:
        keyboard.KeyUp(key)