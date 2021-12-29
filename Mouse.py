from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap

import config


def mouseEvent(type, posx, posy):
    theEvent = CGEventCreateMouseEvent(
                None, 
                type, 
                (posx,posy), 
                kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, theEvent)

def move(posx,posy):
    offset = .25
    o_posx = posx + offset
    flipped = config.W - (o_posx)*config.W
    posx = flipped*(1+2*offset)
    posy = config.H*posy 
    mouseEvent(kCGEventMouseMoved, posx,posy)

def click(posx,posy):
    # uncomment this line if you want to force the mouse 
    # to MOVE to the click location first (I found it was not necessary).
    #mouseEvent(kCGEventMouseMoved, posx,posy);
    mouseEvent(kCGEventLeftMouseDown, posx,posy)
    mouseEvent(kCGEventLeftMouseUp, posx,posy)