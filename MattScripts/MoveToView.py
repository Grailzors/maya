import maya.cmds as mc

'''
MOVE SELECTED ASSETS TO CURRENT CAMERA POSIOTION
'''

def MoveToView():
    currentSel = mc.ls(selection = True)
    camTran = mc.getAttr("%s.translate" % mc.lookThru(query = True))[0]

    for sel in currentSel:
        mc.setAttr("%s.translate" % sel, camTran[0], camTran[1], camTran[2])
        
