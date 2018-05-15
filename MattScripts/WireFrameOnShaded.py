import maya.cmds as mc


def ToggleWireframeOnShaded():
	panel = mc.getPanel(withFocus = True)
	
	if "modelPanel" in panel:
		isWireframe = mc.modelEditor(panel, query = True, wireframeOnShaded = True)
	
		if isWireframe == True:
			mc.modelEditor(panel, edit = True, wireframeOnShaded = False)
		
		else:
			mc.modelEditor(panel, edit = True, wireframeOnShaded = True)