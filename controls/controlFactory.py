import config
import sys

if config.GAME == "SSBB":
    import controls.ssbb_controls as controls

if config.GAME == "PUNCH":
    import controls.punch_controls as controls

if config.GAME == "METROID":
    import controls.metroid_controls as controls

# Interface
actionKeys = []
directionKeys = []
actionsNames = []
actionCnfg = {}

sys.modules[__name__] = controls
