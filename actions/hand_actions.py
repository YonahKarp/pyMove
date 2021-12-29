from joint import Joint2D, noneJoint
from constants import RED
import config

from overlay import putText

def get_orientation(hand : 'list[Joint2D]'):
    wrist, thumb_mid,  thumb, pointer_mid, pointer, middle_mid, \
        middle, index_mid, index, pinky_mid, pinky = hand or [noneJoint] * 11

    span = config.span
    orientations = []
    if(middle_mid.isRightOf(wrist, span*.15) or middle_mid.isLeftOf(wrist, span*.15)):
        orientations.append('horz')
    if(middle_mid.isAbove(wrist, span*.2) or middle_mid.isBelow(wrist, span*.15)):
        orientations.append('vert')
    if(middle_mid.isCloseTo(wrist, span*.2)):
        orientations.append('fwd')

    return orientations


def isTrigger(hand : 'list[Joint2D]'):
    wrist, thumb_mid,  thumb, pointer_mid, pointer, middle_mid, \
        middle, index_mid, index, pinky_mid, pinky = hand or [noneJoint] * 11
    
    orientation = get_orientation(hand)
    isTrigger = False
    if('horz' in orientation):
        isTrigger = isTrigger or wrist.distX(middle) < wrist.distX(middle_mid)*1.25
    if('vert' in orientation):
        isTrigger = isTrigger or wrist.distY(middle) < wrist.distY(middle_mid)*.9
    if('fwd' in orientation):
        isTrigger = isTrigger or wrist.distZ(middle) < wrist.distZ(middle_mid)*1.25

    return isTrigger



   

    
