import xml.etree.ElementTree as xml
import maya.cmds as mc
import os

### Stick in its own module ####
class ProjectData:

	def __init__(self):
		self.rootPath = mc.file(query = True, expandName = True) 
		self.projectPath = self.rootPath.split("scene")[0]
		self.cachePath = os.path.join(self.projectPath, "cache", "lookdev")
		self.texturePath = os.path.join(self.projectPath, "sourceimages")
		self.scenePath = mc.file(query = True, sceneName = True)
		self.sceneName = mc.file(query = True, sceneName = True, shortName = True).split(".")[0]
		self.assetName = self.sceneName.split("_")[0]
		self.cacheName = self.CreateCacheName()


	def CreateDir(self):
		print "Checking DIrectory exists"
		
		if not os.path.exists(self.cachePath):
			print "Creating Path: %s" % (self.cachePath)
			os.makedirs(self.cachePath)   


	def CreateCacheName(self):
		self.CreateDir()
		newName = "Test"

		if os.path.isfile(os.path.join(self.cachePath, self.sceneName)):
			print "Found File :", self.sceneName
			origName = self.sceneName.split(".")[0].split("_", 2)
			newVersion = int(origName[2]) + 1
			newName = "%s_%s_%03d.ma" % (origName[0], origName[1], newVersion)
			print "Made :", newName
		else:
			newName = self.sceneName
		
		return newName


proj = ProjectData()


def main():
	print "Hello World"
	print proj.rootPath
	print proj.cachePath
	print proj.cacheName
	print proj.sceneName
	print proj.assetName

	print "\n### BEGINING LOOKDEV CACHE ###"
	print "------------------------------"
	CheckContext(proj.sceneName)
	CheckShaderName(proj.assetName, GetShaders(GetShadingEngine()))
	SetRelativePath(proj.texturePath)
	ExportShadersXML(proj.cachePath, proj.cacheName, GetShadingEngine(), GetGeo(GetShadingEngine()))

	print "------------------------------"
	print "### LOOKDEV CACHE FINISHED ###'\n"


def CheckContext(assetName):
	root = mc.ls(type = "transform")
	isContext = False
	
	for i in root:
		if i in assetName:
			isContext = True

	if isContext == False:
		mc.warning("Asset is not in context")
		mc.confirmDialog(title = "_('0_0')_ Woops!",
						button = "OK, I will fix it!!!",
						message = "Asset is not in correct context:\n\nContext: %s\n\n* Maya file name is wrong*\n* Top Node name is wrong in outliner*\n\nPlease Fix!" % (assetName))
		mc.warning("Ending LookDev Export Process")
		print "------------------------------"
		exit("LookDev Export Ended Fix Issues")

	print "Context Checked"


def CheckShaderName(assetName , shaders):
	errorList = []

	for i in shaders:
		if assetName not in i:
			errorList.append(i)

	if len(errorList) < 1:
		print "Shader Names Checked"

	else:
		mc.confirmDialog(title = "_('0_0')_ Woops!",
					button = "OK, I will fix it!!!",
					message = "Shaders Inproperly Named:\n\n%s" % (str(errorList)))
		mc.warning("Ending LookDev Export Process")
		print "------------------------------"
		exit("LookDev Export Ended Fix Issues")

def SetRelativePath(texturePath):
	mc.setAttr("defaultArnoldRenderOptions.absoluteTexturePaths", 0)
	mc.setAttr("defaultArnoldRenderOptions.texture_searchpath", texturePath, type = "string")

	print "Relative Path Set"


def GetShadingEngine():
	sg = []

	for i in mc.ls(type = "shadingEngine"):
		if "initial" not in i:
			sg.append(i)

	return sg


def GetShaders(shadingEngine):
	shaders = []

	for i in shadingEngine:
		if mc.listConnections(i, type = "aiStandardSurface"):
			shaders.append(mc.listConnections(i, type = "aiStandardSurface")[0])

		
		if mc.listConnections(i, type = "aiStandardHair"):
			shaders.append(mc.listConnections(i, type = "aiStandardHair")[0])

	return shaders


def GetSets():
	sets = []

	for i in mc.ls(type = "objectSet"):
		if asset in i and "OVERRIDE" in i:
			sets.append(i)

	return sets

def GetGeo(shadingEngine):
	geoSet = []

	for i in shadingEngine:
		mc.select(i, replace = True)
		geoSet = mc.ls(selection = True, flatten = True)
		mc.select(clear = True)

	return geoSet


def RenameShadingEngine():
	pass


def ExportShadersXML(path, cache, shadingEngine, geo):
	root = xml.Element("%s_%s_%s.xml" % (cache.split("_")[0], cache.split("_")[1]+"Shaders", cache.split("_")[2]))

	for i in shadingEngine:
		shadingEngine = xml.SubElement(root, 'ShadingEngine', name = i)
		shader = xml.SubElement(shadingEngine, 'Shader', name = str(i.replace("SG", "")))
		geoSet = xml.SubElement(shader, 'GeoSet', assignment = str(geo))

	#xml.dump(root)

	tree = xml.ElementTree(root)
	tree.write(os.path.join(path, "%s_%s_%s.xml" % (cache.split("_")[0], cache.split("_")[1]+"Shaders", cache.split("_")[2])))

	print "Export Shader Assignments as XML: %s" % (path)

###WORK ON THIS ONE DOESNT WORK###
def ExportSetsXML(path, cache, set, geo):
	root = xml.Element("%s_%s_%s.xml" % (cache.split("_")[0], cache.split("_")[1]+"Sets", cache.split("_")[2]))

	for i in sg:
		shadingEngine = xml.SubElement(root, 'ShadingEngine', name = i)
		shader = xml.SubElement(shadingEngine, 'Shader', name = str(i.replace("SG", "")))
		geoSet = xml.SubElement(shader, 'GeoSet', assignment = str(geo))

	tree = xml.ElementTree(root)
	tree.write(os.path.join(path, "%s_%s_%s.xml" % (cache.split("_")[0], cache.split("_")[1]+"Sets", cache.split("_")[2])))

def ExportShadersMA(path, cache, shadingEngine):
	pass
