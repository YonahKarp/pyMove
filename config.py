import sys
from DolphinControls import Stick

games = ['SSBB', 'PUNCH', 'METROID', "BOXING"]
GAME = games[0] 

DEBUG = True

if(len(sys.argv) > 1):
    DEBUG = sys.argv[1] != 'False'

if(len(sys.argv) >2 ):
    gameIndex = int(sys.argv[2])
    GAME = games[gameIndex]



PAUSED = True
POINTER = False



border = 0
scale = 1/1.5

# Mouse move
H = 1080
W = 1600
h = int(720*scale)
w = int(960*scale)

mouseLocation = (0,0)

sticks = {
    Stick.MAIN: [.5,.5],
    Stick.C: [.5,.5]
}



calibrating = False
calibrated = False
height = .3
mid = .5

span = 0
torso = 0 
h_span = 0
h_height = .7


r_bicep = 0
l_bicep = 0
r_forearm =  0
l_forearm =  0
r_arm = 0
l_arm = 0

l_shoulderX = 0
r_shoulderX = 0



