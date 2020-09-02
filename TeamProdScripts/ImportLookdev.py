import xml.etree.ElementTree as xml
import maya.cmds as mc
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
	print "\n### BEGINING LOOKDEV IMPORT ###"
	print "------------------------------"
	#print "HELLO WORLD"
	#print shot.cachePath
	#print GetLookDevCache()
	lookdevs = LookDevCacheDict(GetLookDevCache())
	lookDevPaths = CacheFilePaths(shot.cachePath, lookdevs)
	print lookdevs
	print lookDevPaths
	#shaders = ParseShaderXML(cachePath)
	#ImportShaders(shaders)
	print "------------------------------"
	print "### LOOKDEV IMPORT FINISHED ###'\n"


def GetLookDevCache():
	cacheList = []

	for i in os.listdir(shot.cachePath):
		if "LookDev" in i:
			cacheList.append(i)

	return cacheList


def GetCacheFiles(path):
	files = []

	for i in os.listdir(path):
		files.append(i)

	return files

def LookDevCacheDict(lookdev):
	dict = {}

	for i in mc.ls("::*_MESH_GRP", type = "transform"):
		for look in lookdev:	
			if i.split("_")[0] in look:
				dict[i] = look

	return dict
	

def ParseOverrideSetsXML():
	pass


def ParseShaderXML(path):
	dict = {} 

	print path

	for p in path:
		print p

		root = xml.parse(p)
		
		for i in root.findall("ShadingEngine"):	
			#THIS '.strip('][').split(',')' recreates the list
			dict[i.attrib["name"]] = { i[0].tag :i[0].attrib["name"], i[0][0].tag : i[0][0].attrib["assignment"].strip('][').split(',') }

	print "Read Shader XML"
	return dict


def ImportShaders(list):
	'''
	importList = []
	
	print "Importing Shaders:"

	for key, value in dict.items():
		if value not in importList:
			importList.append(value)
			cachePath = os.path.join(path, value, "%s.ma" % value)
			mc.file(cachePath, i = True, ignoreVersion = True, type = "mayaAscii", force = True)

			print "Imported Shaders: %s" % value
	'''
	for i in list:
		mc.file(i, i = True, ignoreVersion = True, type = "mayaAscii", force = True)

		print "Imported Shaders: %s" % i		



def CacheFilePaths(path, dict):
	importList = []
	pathsList = []
	print "Creating Cache File Paths"

	for key, value in dict.items():
		if value not in importList:
			importList.append(value)

			## WRONG FILE BEING LOOKED AT GET LOOKDEV CACHE FILE NAME PRP000_LookDevShaders_003.xml ##
			pathsList.append(os.path.join(path, value).replace("\\", "/"))

	return pathsList


def AssignShaders():
	pass


def AssignOverrideSet():
	pass