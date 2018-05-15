import maya.cmds as mc
from functools import partial


def ButtonCommand(name, winID, *args):
	mc.lookThru(name)
	mc.deleteUI(winID)


def CameraListUI():
	winID = "CamListUI"

	if mc.window(winID, 
				query = True, 
				exists = True):
		mc.deleteUI(winID)

	mainWindow = mc.window(winID,
				widthHeight = ( 200, 100), 
				toolbox = True,
				resizeToFitChildren = True)
	mainColumn = mc.columnLayout()
	
	for i in mc.listCameras():
		mc.separator()
		mc.button(i, 
				width = 200,
				command = partial(ButtonCommand, i, winID))

	mc.separator()
		
	mc.showWindow(winID)