import maya.cmds as mc
import pGroupTool.pGroupTools as pgt
from functools import partial


def InstantiateUI():
	winID = "pGroupTool"
	version = "v0.0.1"
	winWidth = 500
	winHeight = 450

	if mc.window(winID, query = True, exists = True):
		mc.deleteUI(winID)
		print "Deleted"
		
	window = mc.window(winID, title = "PolyGroupTool %s" % (version), 
					widthHeight = (winWidth, winHeight),
					resizeToFitChildren = True,
					sizeable = False,
					toolbox = True)

	mainColumn = mc.rowColumnLayout(numberOfColumns = 3)
	mc.separator(parent = mainColumn, width = 10, style = "none")
	column1 = mc.columnLayout(parent = mainColumn, 
					width = winWidth / 2)
	column2 = mc.columnLayout(parent = mainColumn, 
					width = winWidth / 2)

	#Column 1 -------------
	mc.separator(parent = column1, height = 20)
	listField = mc.textScrollList("listField", parent = column1,
			append = pgt.PolyGroupTools().GetPolyGroups(),
			width = 200,
			height = 325)
	mc.separator(parent = column1, height = 10)
	mc.button(label = "Refresh", 
					parent = column1, 
					command = "pGroupTool.pGroupTools.PolyGroupTools().UpdatePolyGroupList()",
					width = 100)


	#Column 2 -------------
	#Additive Controls
	mc.separator(parent = column2, height = 50)
	mc.button(label = "Create pGroup", 
					parent = column2,
					command = "pGroupTool.pGroupTools.PolyGroupTools().CreatePolyGroup()",
					width = 100)

	mc.separator(parent = column2, height = 10)
	mc.button(label = "Add to pGroup", 
					parent = column2,
					command = "pGroupTool.pGroupTools.PolyGroupTools().AddToPolyGroup()",	
					width = 100)

	#Edit Controls
	mc.separator(parent = column2, height = 20)
	renameField = mc.textField("renameField", parent = column2, width = 200)
	mc.button(label = "Rename pGroup", 
					parent = column2, 
					command = "pGroupTool.pGroupTools.PolyGroupTools().RenamePolyGroup()",	
					width = 100)

	mc.separator(parent = column2, height = 10)
	colorColumn = mc.rowColumnLayout(numberOfColumns = 6)
	colorMax = 1
	colorMin = 0

	mc.text("R", width = 15)
	rField = mc.floatField("rField", parent = colorColumn, 
					minValue = colorMin, 
					maxValue = colorMax, 
					precision = 2)
	mc.text("G", width = 15)
	gField = mc.floatField("gField", parent = colorColumn, 
					minValue = colorMin, 
					maxValue = colorMax, 
					precision = 2)
	mc.text("B", width = 15)
	bField = mc.floatField("bField", parent = colorColumn, 
					minValue = colorMin, 
					maxValue = colorMax, 
					precision = 2)
	mc.button(label = "Change Color", parent = column2, width = 100)

	#Destructive Controls
	mc.separator(parent = column2, height = 20)
	mc.button(label = "Merge pGroups", 
					parent = column2, 
					width = 100)

	mc.separator(parent = column2, height = 10)
	mc.button(label = "Delete pGroup", 
					parent = column2,
					command = "pGroupTool.pGroupTools.PolyGroupTools().DeletePolyGroup()",	
					width = 100)


	mc.showWindow(winID)