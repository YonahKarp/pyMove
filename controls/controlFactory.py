import config
import sys

if config.GAME == config.games[0]:
    import controls.ssbb_controls as controls
if config.GAME == config.games[1]:
    import controls.punch_controls as controls
if config.GAME == config.games[2]:
    import controls.metroid_controls as controls
if config.GAME == config.games[3]:
    import controls.boxing_controls as controls

# Interface
actionKeys = []
directionKeys = []
actionsNames = []
actionCnfg = {}

sys.modules[__name__] = controls
