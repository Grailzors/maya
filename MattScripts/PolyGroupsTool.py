import maya.cmds as mc
import random as rand
from functools import partial


class PolyGroupsTool:

	def __init__(self):
		
	def CreatePolyGroup(self):
		sel = mc.ls(selection = True, flatten = True)
		pGroupName = "pGroup1"
		r = rand.uniform(0,1)
		g = rand.uniform(0,1)
		b = rand.uniform(0,1)
		
		if sel:
			mc.select(clear = True)
			pGroup = mc.sets(name = pGroupName + "SG", renderable = True, noSurfaceShader = True)
			pShader = mc.shadingNode('lambert', name = pGroupName, asShader = True)
				
			mc.addAttr(pShader, shortName = "pGroup", attributeType = 'bool')
			mc.setAttr("%s.pGroup" %  (pShader), 1)
			mc.connectAttr("%s.outColor" % (pShader), "%s.surfaceShader" % (pGroup))
			mc.setAttr("%s.color" %  (pShader), r, g, b, type = 'double3')
			
			mc.select(sel, replace = True)
			mc.sets(sel, edit = True, forceElement = pGroup)
			
			self.UpdatePolyGroupList()
		
		def AddToPolyGroup(self, pGroup):
			sel = mc.ls(selection = True)
			
			if sel:
				mc.sets(sel, edit = True, forceElement = pGroup)
				mc.warning("Added selection to %s" % ())
		
		def RenamePolyGroup(self):
			newName = mc.textField(renameField, query = True, text = True)
			oldName = mc.textScrollList(listField, query = True, selectItem = True)[0]
			
			mc.rename(oldName,  newName)
			mc.rename(oldName + "SG", newName + "SG")
			
			self.UpdatePolyGroupList()
			

		def ChangePolyGroupColor(self, pGroup) :
			r = mc.floatField(rField, query = True, value = True)
			g = mc.floatField(gField, query = True, value = True)
			b = mc.floatField(bField, query = True, value = True)
			
			mc.setAttr("%s.color" %  (pGroup), r, g, b, type = 'double3')
			
		def MergePolyGroupd(self):
			#method
		
		def DeletePolyGroup(self):
			#method
		
		def UpdatePolyGroupList(self):
			mc.textScrollList(listField, edit = True, removeAll = True)
			mc.textScrollList(listField, edit = True, append = self.GetPolyGroups())
		
		def GetPolyGroups(self):
			shaders = mc.ls(type = "lambert")
			pGroups = []

			if shaders:
				for i in shaders:
					try:
						if mc.getAttr("%s.pGroup" % (i)):
							pGroups.append(i)
					except:
						continue
						
			return pGroups
		
	def InstantiateUI(self):
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
		listFeild = mc.textScrollList(parent = column1,
                width = 200,
                height = 325)
		mc.separator(parent = column1, height = 10)
		mc.button(label = "Refresh", 
						parent = column1, 
						command = partial(self, UpdatePolyGroupList),
						width = 100)


		#Column 2 -------------
		#Additive Controls
		mc.separator(parent = column2, height = 50)
		mc.button(label = "Create pGroup", 
						parent = column2, 
						width = 100)

		mc.separator(parent = column2, height = 10)
		mc.button(label = "Add to pGroup", 
						parent = column2, 
						width = 100)

		#Edit Controls
		mc.separator(parent = column2, height = 20)
		renameField = mc.textField("test", parent = column2, width = 200)
		mc.button(label = "Rename pGroup", 
						parent = column2, 
						command = partial(self, RenamePolyGroup),
						width = 100)

		mc.separator(parent = column2, height = 10)
		colorColumn = mc.rowColumnLayout(numberOfColumns = 6)
		colorMax = 1
		colorMin = 0

		mc.text("R", width = 15)
		rField = mc.floatField(parent = colorColumn, 
						minValue = colorMin, 
						maxValue = colorMax, 
						precision = 2)
		mc.text("G", width = 15)
		gField = mc.floatField(parent = colorColumn, 
						minValue = colorMin, 
						maxValue = colorMax, 
						precision = 2)
		mc.text("B", width = 15)
		bField = mc.floatField(parent = colorColumn, 
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
						width = 100)


		mc.showWindow(winID)
		