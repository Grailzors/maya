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
	print "HELLO WORLD"
	print shot.cachePath
	print GetLookDevCache()


def GetLookDevCache():
	cacheList = []

	for i in os.listdir(shot.cachePath):
		if "LookDev" in i:
			cacheList.append(i)

	return cacheList


def GetAssets():
	pass


def ParseOverrideSetsXML():
	pass


def ParseShaderXML():
	pass


def ImportShaders():
	pass


def AssignShaders():
	pass