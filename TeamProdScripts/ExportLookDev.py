import xml.etree.ElementTree as xml
import maya.cmds as mc
import os

### Stick in its own module ####
class AssetData:

	def __init__(self):
		self.rootPath = mc.file(query = True, expandName = True) 
		self.projectPath = self.rootPath.split("scene")[0]
		self.cachePath = os.path.join(self.projectPath, "cache", "lookdev")
		self.texturePath = os.path.join(self.projectPath, "sourceimages")
		self.scenePath = mc.file(query = True, sceneName = True)
		self.sceneName = mc.file(query = True, sceneName = True, shortName = True).split(".")[0]
		self.assetName = self.sceneName.split("_")[0]
		self.cacheName = self.CreateCacheName()

		self.CreateDir()


	def CreateDir(self):
		print "Checking Directory exists"
		
		if not os.path.exists(os.path.join(self.cachePath, self.cacheName)):
			print "Creating Path: %s" % (os.path.join(self.cachePath, self.cacheName))
			os.makedirs(os.path.join(self.cachePath, self.cacheName))   


	def CreateCacheName(self):
		#self.CreateDir()
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


asset = AssetData()


def main():
	print "\n### BEGINING LOOKDEV CACHE ###"
	print "------------------------------"
	CheckContext(asset.sceneName)
	CheckShaderName(asset.assetName, GetShaders(GetShadingEngine()))
	SetRelativePath(asset.texturePath)
	RenameShadingEngine(GetShadingEngine())
	ExportShadersXML(asset.cachePath, asset.cacheName, GetShadingEngine())
	ExportSetsXML(asset.cachePath, asset.cacheName, GetSets(asset.assetName))
	ExportShadersMA(asset.cachePath, asset.cacheName, GetShadingEngine())
	print "------------------------------"
	print  "Export Location:", asset.cachePath.replace("\\", "/")
	print "### LOOKDEV CACHE FINISHED ###'\n"

	OutputExportLocation()


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
		if "SRF_%s" % (assetName) not in i and "FUR_%s" % (assetName) not in i: 
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
	typeList = ["aiLayerShader", "aiMixShader", "aiStandardSurface", "aiStandardHair"] 

	for engine in shadingEngine:
		for type in typeList:
			if mc.listConnections(engine, type = type):
				shaders.append(mc.listConnections(engine, type = type)[0])

	return shaders


def GetSets(asset):
	sets = []

	for i in mc.ls(type = "objectSet"):
		if asset in i and "OVERRIDE" in i:
			sets.append(i)

	return sets


def GetGeo(set):
	geoSet = []

	if set:
		mc.select(set, replace = True)
		geoSet = (mc.ls(selection = True, flatten = True))
		mc.select(clear = True)

	return geoSet


def GetOverrideAttr(set, parent):
		for i in mc.listAttr(set, userDefined = True):
			xml.SubElement(parent, "Attribute", name = "%s.%s" % (set, i), value = str(mc.getAttr("%s.%s" % (set, i))))


def RenameShadingEngine(shadingEngine):
	for i in shadingEngine:
		newName = ""

		for t in ["aiLayerShader", "aiMixShader", "aiStandardSurface", "aiStandardHair"]:
			if mc.listConnections(i, type = t):
				#print mc.listConnections(i, type = "aiStandardSurface")[0]
				newName = mc.listConnections(i, type = t)[0] + "SG"

		if i not in newName:
			mc.rename(i, newName)
			print "--- Renamed Shading Groups Start ---"
			print "%s ---> %s" % (i, newName)
			print "--- Renamed Shading Groups End ---"

	sEngine = GetShadingEngine()


def OutputExportLocation():
	mc.confirmDialog(title = "_( ^_^ )_ %s Exported!" % (asset.assetName),
		button = "Woot!!!",
		message = "# Asset Export Succesful #\n\n%s" % (asset.cachePath.replace("\\", "/")))


def ExportShadersXML(path, cache, shadingEngine):
	root = xml.Element("%s_%s_%s.xml" % (cache.split("_")[0], cache.split("_")[1]+"Shaders", cache.split("_")[2]))

	for i in shadingEngine:
		se = xml.SubElement(root, 'ShadingEngine', name = i)
		shader = xml.SubElement(se, 'Shader', name = str(i.replace("SG", "")))
		geometry = xml.SubElement(shader, 'Geo', assignment = str(GetGeo(i)))

	#xml.dump(root)

	tree = xml.ElementTree(root)
	tree.write(os.path.join(path, cache, "%s_%s_%s.xml" % (cache.split("_")[0], cache.split("_")[1]+"Shaders", cache.split("_")[2])))

	print "Expored Shader Assignments as XML"


def ExportSetsXML(path, cache, geoSet):
	if geoSet:
		root = xml.Element("%s_%s_%s.xml" % (cache.split("_")[0], cache.split("_")[1]+"Sets", cache.split("_")[2]))


		for i in geoSet:
			gs = xml.SubElement(root, 'OverrideSet', name = i)
			GetOverrideAttr(i, gs)
			geometry = xml.SubElement(gs, 'Geo', assignment = str(GetGeo(i)))

		#xml.dump(root)

		tree = xml.ElementTree(root)
		tree.write(os.path.join(path, cache, "%s_%s_%s.xml" % (cache.split("_")[0], cache.split("_")[1]+"Sets", cache.split("_")[2])))

		print "Export Override Sets as XML"


def ExportShadersMA(path, cache, shadingEngine):
	mc.select(shadingEngine, replace = True, noExpand = True)
	mc.file(os.path.join(path, cache, cache + ".ma"), 
			force = True,
			type = "mayaAscii", 
			preserveReferences = True,
			exportSelected = True)
	mc.select(clear = True)

	print "Exported LookDev Shaders"