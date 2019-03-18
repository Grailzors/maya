import maya.cmds as mc
import random as rand


class PolyGroupTools(object):

	def _init_(self):
		print "Initializing pGroups Tool"
		self.UpdatePolyGroupList()
		
	def CreatePolyGroup(self):
		sel = mc.ls(selection = True, flatten = True)
		pGroupName = "pGroup1"
		r = rand.uniform(0,1)
		g = rand.uniform(0,1)
		b = rand.uniform(0,1)
		
		if sel:
			mc.select(clear = True)
			pShader = mc.shadingNode('lambert', name = pGroupName, asShader = True)			
			pGroup = mc.sets(name = pShader + "SG", renderable = True, noSurfaceShader = True)
			
			mc.addAttr(pShader, shortName = "pGroup", attributeType = 'bool')
			mc.setAttr("%s.pGroup" %  (pShader), 1)
			mc.connectAttr("%s.outColor" % (pShader), "%s.surfaceShader" % (pGroup))
			mc.setAttr("%s.color" %  (pShader), r, g, b, type = 'double3')
			
			mc.select(sel, replace = True)
			mc.sets(sel, edit = True, forceElement = pGroup)
			
			self.UpdatePolyGroupList()
		
	def AddToPolyGroup(self):
		sel = mc.ls(selection = True)
		
		if sel:
			mc.sets(sel, edit = True, forceElement = "%sSG" % (mc.textScrollList("listField", query = True, selectItem = True)[0]))
			mc.warning("Added selection to %s" % (mc.textScrollList("listField", query = True, selectItem = True)[0]))
	
	def SelectPolyGroupItems(self):
		print ""
	
	def RenamePolyGroup(self):
		newName = mc.textField("renameField", query = True, text = True)
		oldName = mc.textScrollList("listField", query = True, selectItem = True)[0]
		
		print oldName, newName
		
		mc.rename(oldName,  newName)
		mc.rename(oldName + "SG", newName + "SG")
		
		self.UpdatePolyGroupList()
		
	def ChangePolyGroupColor(self, pGroup) :
		r = mc.floatField("rField", query = True, value = True)
		g = mc.floatField("gField", query = True, value = True)
		b = mc.floatField("bField", query = True, value = True)
		
		mc.setAttr("%s.color" %  (pGroup), r, g, b, type = 'double3')
	
	def MergePolyGroupd(self):
		print ''

	def DeletePolyGroup(self):
		sel = mc.textScrollList("listField", query = True, selectItem = True) 		
		pGroup = mc.ls(mc.sets(sel, query = True), flatten = True)
		
		for i in sel:
			mc.sets(i + "SG", edit = True, forceElement = "initialShadingGroup")
			mc.delete(i)
			mc.delete(i + "SG")

	def UpdatePolyGroupList(self):		
		if mc.textScrollList("listField", query = True, exists = True):
			mc.textScrollList("listField", edit = True, removeAll = True)
			mc.textScrollList("listField", edit = True, append = self.GetPolyGroups())

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

	def Test(self):
		print "Success"
