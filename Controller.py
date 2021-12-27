
from ssbb_controls import actionCnfg, actionKeys, directionKeys
from Keyboard import keyboard
import Mouse as mouse
from threading import Timer
import config as cnfg

from ssbb_controls import actionCnfg, directionKeys, actionsNames





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
                    keyboard.KeyDown(key)
                    keyCheck[key] = True

                    if(multi and not keyCheck[otherKey]):
                        keyboard.KeyDown(otherKey)
                        keyCheck[otherKey] = True

                else:
                    if(not self.actionCheck[action]):
                        if(multi and not keyCheck[otherKey]):
                            if otherKey in directionKeys:
                                for k in directionKeys:
                                    if not config.keepDirection == k:
                                        keyboard.KeyUp(k)

                            keyboard.KeyDown(otherKey)
                            Timer(0.25, self.cancelPress, (otherKey,)).start()
                        
                        keyboard.KeyDown(key)
                        Timer(0.25, self.cancelPress, (key, action)).start()
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
        

    def cancelPress(self, key, action = None):
        keyboard.KeyUp(key)
        if action:
            self.actionCheck[action] = False


controller = Controller()
