import config
import sys

if config.GAME == "SSBB":
    import actions.ssbb_actions as actions
if config.GAME == "PUNCH":
    import actions.punch_actions as actions


# Interface
def pointerActions():pass
def checkForActions():pass
def pauseActions(): pass
def calibrate(): pass


sys.modules[__name__] = actions
