import config
import sys

if config.GAME == config.games[0]:
    import actions.ssbb_actions as actions
if config.GAME == config.games[1]:
    import actions.punch_actions as actions
if config.GAME == config.games[2]:
    import actions.metroid_actions as actions
if config.GAME == config.games[3]:
    import actions.boxing_actions as actions


# Interface
def pointerActions():pass
def checkForActions():pass
def pauseActions(): pass
def calibrate(): pass


sys.modules[__name__] = actions
