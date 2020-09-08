import xml.etree.ElementTree as xml
import maya.cmds as mc
import maya.mel as mm
import os


class AssetData():

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
		

		if not os.path.exists(self.cachePath):
			path = str(self.cachePath)
			print "Creating Path: %s" % self.cachePath
			os.makedirs(path)


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


shot = AssetData()


def main():
	lookdevDict = GetLookDevCacheDict(shot.cachePath)
	shaderDict = ParseShaderXML(shot.cachePath, lookdevDict)
	setDict = 	ParseSetsXML(shot.cachePath, lookdevDict)

	print "\n### BEGINING LOOKDEV IMPORT ###"
	print "------------------------------"

	ImportShaders(shot.cachePath, lookdevDict)
	ConnectShaders(shaderDict) 
	AssignShaders(shaderDict)
	AssignOverrideSets(setDict)

	print "--- Cleaning Nodes ---"
	mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
	print "--- Nodes Cleaned ---"

	print "------------------------------"
	print "### LOOKDEV IMPORT FINISHED ###'\n"


def GetLookDevCacheDict(path):
	files = []
	
	for cache in os.listdir(path):
		dict = {}
		dict[cache] = {"maXML" : "", "SetsXML" : "", "ShaderXML" : ""}
		
		if "LookDev" in cache:
			for file in os.listdir(os.path.join(path, cache)):
				if ".ma" in file:
					dict[cache]["maXML"] = file
				if "Sets" in file:	
					dict[cache]["SetsXML"] = file
				if "Shader" in file:
					dict[cache]["ShaderXML"] = file

		files.append(dict)

	print "Got LookDev Caches"
	return files


def ParseShaderXML(path, dict):
	xmlDict = {}

	for i in dict:
		for k, v in i.items():
			root = xml.parse(os.path.join(path, k, v["ShaderXML"]).replace("\\", "/"))
			
			for i in root.findall("ShadingEngine"):	
				#THIS '.strip('][').split(',')' recreates the list
				xmlDict[i.attrib["name"]] = { i[0].tag :i[0].attrib["name"], i[0][0].tag : i[0][0].attrib["assignment"].strip('][').split(',') }

	print "Read Shader XML"
	return xmlDict


def ParseSetsXML(path, dict):
	xmlDict = {}

	for i in dict:
		for k, v in i.items():
			root = xml.parse(os.path.join(path, k, v["SetsXML"]).replace("\\", "/"))
			
			for i in root.findall("OverrideSet"):	
				#print "Geo", i[3].attrib["assignment"]

				xmlDict[i.attrib["name"]] = { i[0].attrib["name"] : i[0].attrib["value"],
											i[1].attrib["name"] : i[1].attrib["value"],
											i[2].attrib["name"] : i[2].attrib["value"], 
											"Geo" : i[3].attrib["assignment"].strip('][').split(',')
											}

	print "Read Sets XML"
	return xmlDict


def ImportShaders(path, dict):
	for i in dict:
		for k, v in i.items():
			file = os.path.join(path, k, v["maXML"]).replace("\\", "/")
			
			mc.file(file, i = True, ignoreVersion = True, type = "mayaAscii", force = True)

			print "Imported Shaders: %s" % v["maXML"]


def ConnectShaders(dict):
	print "--- Connecting Shaders ---"
	
	for k, v in dict.items():
		mc.connectAttr("%s.outColor" % v["Shader"], "%s.surfaceShader" % k, force = True)
		print v["Shader"], "---->", k

	print "--- Connecting Shaders Done! ---"


def AssignShaders(dict):
	mc.select(clear = True)

	print "--- Assigning Shaders to Geo ---"

	for k, v in dict.items():		
		print "Assigning:", v["Shader"]

		if len(v["Geo"]) > 1:
			for a in v["Geo"]:
				name = a.split("'")[1]
				asset = "::%s_%s*" % (name.split("_")[0], name.split("_")[1])

				for i in mc.ls(asset, type = "shape"):
					if ":" in i:
						ns = i.split(":")[0]
						geo = "%s:%s" % (ns, name)
						#print "GEO:", geo
						
						mc.sets(geo, forceElement = k)

					else:
						mc.sets(i, forceElement = k)
						#print name

	print "--- Shaders Assigned  ---"


def AssignOverrideSets(dict):
	mc.select(clear = True)

	for k, v in dict.items():
		if mc.objExists(k) == False:
			mc.sets(name = k, empty = True)

		for attr, value in v.items(): 
			mc.select(k, noExpand = True, replace = True)
			if "OVERRIDE" in attr:
				if mc.attributeQuery(attr.split(".")[1], node =  attr.split(".")[0], exists = True) == False:
					mc.addAttr(shortName = attr.split(".")[1], category = "arnold", defaultValue = int(value))

				mc.select(clear = True)

			elif "Geo" in attr:			
				for v in value:
					geo = "::%s_%s*" % (v.strip("u'").split("_")[0], v.strip("u'").split("_")[1])
				
					for shape in mc.ls(geo, type = "shape"):
						if ":" in shape:
							mc.sets(shape, forceElement = k)

					mc.sets(geo, forceElement = k)

	print "--- Override Sets Assigned  ---"