
from controls.controlFactory import actionCnfg, actionKeys, directionKeys, actionsNames
from Keyboard import keyboard
import Mouse as mouse
from threading import Timer
import config as cnfg





class Controller():

    def __init__(self):
        self.actionCheck = dict(zip(actionsNames, [0]*len(actionsNames)))

    def handlePresses(self,actions):
        keyCheck = dict(zip(actionKeys, [0]*len(actionKeys)))

        deadActions = []
        if('move mouse' in actions):
            coords = cnfg.mouseLocation
            mouse.move(*coords)

        for action in actionsNames:
            config = actionCnfg[action]
            key, sustain, multi, otherKey = config.params()

            if action in actions:
                
                if(sustain):
                     # first key
                    if(config.delay and not self.actionCheck[action]):
                        Timer(config.delay, self.pressKey, (key, action)).start()
                        self.actionCheck[action] = True
                    else:           
                        keyboard.KeyDown(key)
                    keyCheck[key] = True

                    if(multi and not keyCheck[otherKey]):
                        keyboard.KeyDown(otherKey)
                        keyCheck[otherKey] = True

                else:
                    if(not self.actionCheck[action]):
                        # first key
                        if(config.delay > 0):
                            Timer(config.delay, self.pressKey, (key)).start()
                        else:           
                            keyboard.KeyDown(key)
                        Timer(0.20-config.delay, self.cancelPress, (key, action)).start()

                        # other key
                        if(multi and not keyCheck[otherKey]):
                            if otherKey in directionKeys:
                                for k in directionKeys:
                                    if not config.keepDirection == k:
                                        keyboard.KeyUp(k)

                            keyboard.KeyDown(otherKey)
                            Timer(0.20, self.cancelPress, (otherKey,)).start()

                        
                        self.actionCheck[action] = True

                    keyCheck[key] = True
                    if(multi):  keyCheck[otherKey] = True


            else:
                deadActions.append(action)

        # second loop becuase we don't want to KeyUp before we know all action input
        for action in deadActions:
            config = actionCnfg[action]

            key, sustain, multi, otherKey = config.params()

            if not keyCheck[key]:
                keyboard.KeyUp(key)

            if(multi and not keyCheck[otherKey]):
                keyboard.KeyUp(otherKey)
        

    def pressKey(self, key, action = None):
        keyboard.KeyDown(key)
        if action:
            self.actionCheck[action] = False

    def cancelPress(self, key, action = None):
        keyboard.KeyUp(key)
        if action:
            self.actionCheck[action] = False


controller = Controller()
