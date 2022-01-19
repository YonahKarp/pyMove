class Action():
    def __init__(self, key, sustain=False, 
        multi=False, otherKey=None, keepDirection=None, delay = 0,
        isStick= False
        ):
        self.key = key
        self.sustain = sustain
        self.multi = multi
        self.otherKey = otherKey
        self.keepDirection = keepDirection
        self.delay = delay
        self.isStick = isStick

    def params(self):
        return (self.key, self.sustain, self.multi, self.otherKey)