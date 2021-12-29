from joint import Joint2D

def shouldPause(r_wrist: Joint2D, l_wrist: Joint2D, head: Joint2D, span):
  return (r_wrist.distX(l_wrist) < span  and r_wrist.distY(l_wrist) < span 
      and r_wrist.isAbove(head, span*.4) and l_wrist.isAbove(head, span*.4))

def shouldCalibrate(r_wrist: Joint2D, l_wrist: Joint2D, r_shoulder: Joint2D, l_shoulder: Joint2D, r_arm, l_arm):
  return (r_wrist.isRightOf(r_shoulder, r_arm*.9) and l_wrist.isLeftOf(l_shoulder, l_arm*.9))

def shouldPoint(r_wrist: Joint2D, l_wrist: Joint2D, head: Joint2D, span):
    return (r_wrist.distX(l_wrist) > span*2 and r_wrist.distY(l_wrist) < span
      and r_wrist.isAbove(head) and l_wrist.isAbove(head))