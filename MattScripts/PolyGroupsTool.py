import maya.cmds as mc
import random as rand


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
			
			mc.connectAttr("%s.outColor" % (pShader), "%s.surfaceShader" % (pGroup))
			mc.setAttr("%s.color" %  (pShader), r, g, b, type = 'double3',)
			
			mc.select(sel, replace = True)
			mc.sets(sel, edit = True, forceElement = pGroup)
		
		
	def InstantiateUI(self):
		winID = "pGroupTool"
		
		