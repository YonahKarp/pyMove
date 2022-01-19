
from controls.controlFactory import actionCnfg, actionKeys, directionKeys, actionsNames
# from Keyboard import keyboard
from DolphinControls import dolphinControls
import Mouse as mouse
from threading import Timer
import config as cnfg





class PipeController():

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
            button, sustain, multi, otherButton = config.params()

            if action in actions:        
                if(sustain):
                    if(config.isStick): #stick should only be first key
                        x,y = cnfg.sticks[button]
                        dolphinControls.set_stick(button, x,y)
                        keyCheck[button] = True
                    else:            
                        dolphinControls.press_button(button)           
                        keyCheck[button] = True

                    if(multi and not keyCheck[otherButton]):
                        dolphinControls.press_button(otherButton)           
                        keyCheck[otherButton] = True

                else:
                    if(not self.actionCheck[action]):
                        # first key
                        # if(config.delay > 0):
                        #     Timer(config.delay, self.pressButton, (button)).start()
                        # else:           
                        #     dolphinControls.press_button(button)
                        if(config.isStick): #stick should only be first key
                            x,y = cnfg.sticks[button]
                            dolphinControls.set_stick(button, x,y)
                            Timer(config.delay or .2, self.cancelStick, (button, action)).start()
                        else:
                            dolphinControls.press_button(button)
                            Timer(config.delay or .2, self.cancelPress, (button, action)).start()


                        # other key
                        if(multi and not keyCheck[otherButton]):
                            dolphinControls.press_button(otherButton)
                            Timer(config.delay or .2, self.cancelPress, (otherButton,)).start()
                        
                        self.actionCheck[action] = True

                    keyCheck[button] = True
                    if(multi):  keyCheck[otherButton] = True

        # second loop becuase we don't want to KeyUp before we know all action input

        for button in actionKeys:
            if not keyCheck[button]:
                if button.name == 'MAIN' or button.name == 'C':
                    dolphinControls.reset_stick(button)
                else:
                    dolphinControls.release_button(button)
        

    # def pressButton(self, key, action = None):
    #     keyboard.KeyDown(key)
    #     if action:
    #         self.actionCheck[action] = False

    def cancelStick(self, stick, action = None):
        dolphinControls.reset_stick(stick)
        if action:
            self.actionCheck[action] = False

    def cancelPress(self, button, action = None):
        dolphinControls.release_button(button)
        if action:
            self.actionCheck[action] = False


controller = PipeController()
