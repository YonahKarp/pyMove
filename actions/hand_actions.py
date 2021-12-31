from joint import Joint2D, noneJoint
from constants import RED
import config
import math

from overlay import putText

def get_orientation(hand : 'list[Joint2D]', frame=None):
    wrist, thumb_mid,  thumb, pointer_mid, pointer, middle_mid, \
        middle, index_mid, index, pinky_mid, pinky = hand or [noneJoint] * 11

    fingerSpan = max(thumb.distX(pinky), thumb.distY(pinky), pointer_mid.distY(pinky_mid), config.span*.2)
    span = config.span
    orientations = []
    vertical = False
    horizontal = False

    orientations = {'up':False, 'down':False, 'horz':False, 'flat': False, 'fwd up':False, 'fwd down':False, }

    if(middle_mid.isRightOf(wrist, span*.15) or middle_mid.isLeftOf(wrist, span*.15)):
        if frame is not None: putText(frame, 'horz', (.5,.7), RED)
        orientations['horz'] = True
    elif(middle_mid.isAbove(wrist, fingerSpan*.2)):
        if frame is not None: putText(frame, 'up', (.5,.8), RED)
        orientations['up'] = True
        vertical = True
    elif(middle_mid.isBelow(wrist, fingerSpan*.15)):
        if frame is not None: putText(frame, 'down', (.5,.8), RED)
        orientations['down'] = True
    

    if(vertical and thumb.distX(pinky) < fingerSpan*.2
      or horizontal and thumb.distY(pinky) < fingerSpan*.2):
        orientations['flat'] = True

    if(
        middle_mid.isCloseTo(wrist, span*.2)
        # middle.distZ(wrist) > fingerSpan
    ):
        dir = 'fwd up' if(middle_mid.isAbove(wrist)) else 'fwd dwn'
        if frame is not None: putText(frame, dir, (.5,.6), RED)
        orientations[dir] = True

    return orientations



def isTrigger(hand : 'list[Joint2D]', frame=None):
    wrist, thumb_mid,  thumb, pointer_mid, pointer, middle_mid, \
        middle, index_mid, index, pinky_mid, pinky = hand or [noneJoint] * 11


    fingerSpan = max(thumb.distX(pinky), thumb.distY(pinky), pointer_mid.distY(pinky_mid), config.span*.2)

    
    orientation = get_orientation(hand, frame)
    isTrigger = False
    # if(orientation['horz']):
    #     isTrigger = isTrigger or wrist.distX(middle) < wrist.distX(middle_mid) + fingerSpan*.1
    if(orientation['up'] or orientation['horz']):
        isTrigger = isTrigger or middle.isBelow(middle_mid, fingerSpan*.2)
    if(orientation['fwd up']):
        isTrigger = False#isTrigger or middle.isBelow(wrist, fingerSpan*.5)

    return isTrigger

def isFist(hand : 'list[Joint2D]', frame=None):
    wrist, thumb_mid,  thumb, pointer_mid, pointer, middle_mid, \
        middle, index_mid, index, pinky_mid, pinky = hand or [noneJoint] * 11

    orientation = get_orientation(hand)
    trigger = isTrigger(hand)
    # putText(frame, str(trigger), (.5,.6), RED)

    if not trigger:
        return False

    isFist = False

    # if(orientation['horz']):
    #     if(orientation['flat']):
    #         isFist = isFist or thumb.isBelow(middle)
    #     else:
    #         isFist = isFist or thumb.isBelow(thumb_mid)

    if(orientation['up'] and not orientation['horz']):
        isFist = isFist or (thumb.isRightOf(pointer_mid, 0) and pointer.isBelow(thumb))

    
    return isFist





def get_orientation2(hand : 'list[Joint2D]', frame=None):
    wrist, thumb_mid,  thumb, pointer_mid, pointer, middle_mid, \
        middle, index_mid, index, pinky_mid, pinky = hand or [noneJoint] * 11


    vertical = None
    horizontal = None
    flat = False
    fwd = False


    span = config.span
    fingerSpan = max(thumb.distX(pinky), thumb.distY(pinky))

    if(middle_mid.isAbove(wrist, span*.2)):
        vertical = 'up'
    elif(middle_mid.isRightOf(wrist, span*.15)):
        horizontal = 'right'
    elif(middle_mid.isLeftOf(wrist, span*.15)):
        horizontal = 'left'
    elif(middle_mid.isBelow(wrist, span*.15)):
        vertical = 'down'


    if(vertical and thumb.distX(pinky) < span*.2
      or horizontal and thumb.distY(pinky) < span*.2):
        flat = True
    elif( middle_mid.isCloseTo(wrist, span*.2)):
        fwd = True

    
    if frame is not None and flat: putText(frame, 'flat', (.5,.4), RED)
    if frame is not None and fwd: putText(frame, 'fwd', (.5,.6), RED)
    if frame is not None and horizontal: putText(frame, horizontal, (.5,.7), RED)
    if frame is not None and vertical: putText(frame, vertical, (.5,.8), RED)


        


# def __getEuclideanDistance(self, posA, posB):
#     return math.sqrt((posA.x - posB.x)**2 + (posA.y - posB.y)**2)

# def __isThumbNearIndexFinger(self, thumbPos, indexPos):
#     return self.__getEuclideanDistance(thumbPos, indexPos) < 0.1


# def detectFingers(self, hand, axis='x', flat=False, dir=1):
#     fingers = hand or [noneJoint] * 11

    
#     wrist1, thumb_mid1,  thumb1, pointer_mid1, pointer1, middle_mid1, middle1, index_mid1, index1, pinky_mid1, pinky1 = \
#         [finger.x for finger in hand] if axis == 'x' else [finger.y for finger in hand]



    

#     thumbIsOpen = False
#     indexIsOpen = False
#     middelIsOpen = False
#     ringIsOpen = False
#     pinkyIsOpen = False

#     pseudoFixKeyPoint = handLandmarks[2].x
#     if handLandmarks[3].x < pseudoFixKeyPoint and handLandmarks[4].x < pseudoFixKeyPoint:
#         thumbIsOpen = True

#     pseudoFixKeyPoint = handLandmarks[6].y
#     if handLandmarks[7].y < pseudoFixKeyPoint and handLandmarks[8].y < pseudoFixKeyPoint:
#         indexIsOpen = True

#     pseudoFixKeyPoint = handLandmarks[10].y
#     if handLandmarks[11].y < pseudoFixKeyPoint and handLandmarks[12].y < pseudoFixKeyPoint:
#         middelIsOpen = True

#     pseudoFixKeyPoint = handLandmarks[14].y
#     if handLandmarks[15].y < pseudoFixKeyPoint and handLandmarks[16].y < pseudoFixKeyPoint:
#         ringIsOpen = True

#     pseudoFixKeyPoint = handLandmarks[18].y
#     if handLandmarks[19].y < pseudoFixKeyPoint and handLandmarks[20].y < pseudoFixKeyPoint:
#         pinkyIsOpen = True

#     if thumbIsOpen and indexIsOpen and middelIsOpen and ringIsOpen and pinkyIsOpen:
#         print("FIVE!")

#     elif not thumbIsOpen and indexIsOpen and middelIsOpen and ringIsOpen and pinkyIsOpen:
#         print("FOUR!")

#     elif not thumbIsOpen and indexIsOpen and middelIsOpen and ringIsOpen and not pinkyIsOpen:
#         print("THREE!")

#     elif not thumbIsOpen and indexIsOpen and middelIsOpen and not ringIsOpen and not pinkyIsOpen:
#         print("TWO!")

#     elif not thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and not pinkyIsOpen:
#         print("ONE!")

#     elif not thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and pinkyIsOpen:
#         print("ROCK!")

#     elif thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and pinkyIsOpen:
#         print("SPIDERMAN!")

#     elif not thumbIsOpen and not indexIsOpen and not middelIsOpen and not ringIsOpen and not pinkyIsOpen:
#         print("FIST!")

#     elif not indexIsOpen and middelIsOpen and ringIsOpen and pinkyIsOpen and self.__isThumbNearIndexFinger(handLandmarks[4], handLandmarks[8]):
#         print("OK!")

#         print("FingerState: thumbIsOpen? " + str(thumbIsOpen) + " - indexIsOpen? " + str(indexIsOpen) + " - middelIsOpen? " +
#             str(middelIsOpen) + " - ringIsOpen? " + str(ringIsOpen) + " - pinkyIsOpen? " + str(pinkyIsOpen))




