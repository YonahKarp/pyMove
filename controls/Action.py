class Action():
    def __init__(self, key, sustain=False, multi=False, otherKey=None, keepDirection=None):
        self.key = key
        self.sustain = sustain
        self.multi = multi
        self.otherKey = otherKey
        self.keepDirection = keepDirection

    def params(self):
        return (self.key, self.sustain, self.multi, self.otherKey)