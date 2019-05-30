import maya.cmds as mc
from functools import partial

def AddConstant(*arg):
    sel = mc.ls(selection = True)
    
    if sel:
        for i in sel:
            mesh = mc.pickWalk(i, direction = "down")[0]
            
            if mc.attributeQuery("mtoa_constant_color", node = mesh, exists = True) == False:
                objectColor =  mc.colorSliderGrp("objectColor", query = True, rgbValue = True)
                
                print mesh
                mc.addAttr(longName = "mtoa_constant_color", usedAsColor = True, attributeType = "float3")
                mc.addAttr(longName = "arnoldColorR", attributeType = "float", parent = "mtoa_constant_color")
                mc.addAttr(longName = "arnoldColorG", attributeType = "float", parent = "mtoa_constant_color")
                mc.addAttr(longName = "arnoldColorB", attributeType = "float", parent = "mtoa_constant_color")
                
                mc.setAttr("%s.arnoldColorR" % (mesh), objectColor[0])
                mc.setAttr("%s.arnoldColorG" % (mesh), objectColor[1])
                mc.setAttr("%s.arnoldColorB" % (mesh), objectColor[2])
                
        mc.select(sel, replace = True)
        UpdateConstantList()

def GetOpaque(*arg):
    sel = mc.ls(selection = True)
    
    if sel:
        for i in sel:
            i = mc.pickWalk(i, direction = "down")[0]
            return mc.getAttr("%s.aiOpaque" % i)
    
    mc.select(sel, replace = True)

def SetOpaque(*arg):
    print ""

def GetMatte(*arg):
    sel = mc.ls(selection = True)
    
    if sel:
        for i in sel:
            i = mc.pickWalk(i, direction = "down")[0]
            return mc.getAttr("%s.aiMatte" % i)
            
    mc.select(sel, replace = True)

def SetMatte(*arg):
    print ""

def GetColor(*arg):
    #This is for getting the color from a already set color in the mtoa list
    print ""

def UpdateColor(*arg):
    objectColor =  mc.colorSliderGrp("objectColor", query = True, rgbValue = True)
    
    if mc.textScrollList("listField", query = True, exists = True):        
        for i in mc.textScrollList("listField",  query = True, selectItem = True):
            print i
            mc.setAttr("%s.arnoldColorR" % (i), objectColor[0])
            mc.setAttr("%s.arnoldColorG" % (i), objectColor[1])
            mc.setAttr("%s.arnoldColorB" % (i), objectColor[2])

def GetConstantObjects(*arg):
    mesh = mc.ls(type = "mesh")
    meshList = []

    if mesh:
        for i in mesh:
            try:
                if mc.getAttr("%s.mtoa_constant_color" % (i)):
                    meshList.append(i)
            except:
                continue

    return meshList

def UpdateConstantList(*arg):
    if mc.textScrollList("listField", query = True, exists = True):
        mc.textScrollList("listField", edit = True, removeAll = True)
        mc.textScrollList("listField", edit = True, append = GetConstantObjects())
    
def InstantiateUI():
	winID = "constantTool"
	version = "v0.0.1"
	winWidth = 420
	winHeight = 450

	if mc.window(winID, query = True, exists = True):
		mc.deleteUI(winID)
		print "Deleted"
		
	window = mc.window(winID, title = "MtoA Object Control Panel %s" % (version), 
					widthHeight = (winWidth, winHeight),
					resizeToFitChildren = True,
					#sizeable = False,
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
            allowMultiSelection = True,
			append = GetConstantObjects(),
			width = 200,
			height = 325)
	mc.separator(parent = column1, height = 10)
	mc.button(label = "Refresh", 
					parent = column1, 
					command = partial(UpdateConstantList),
					width = 100)
					
	#Column 2 -------------
	#Render Stats
	mc.separator(parent = column2, height = 20)
	
	mc.text("Render Stats", parent=column2, enable=False)
	mc.separator(parent = column2, height = 10)
	mc.button(label="Add mtoa_constant_color",
                    command = partial(AddConstant))
	mc.separator(parent = column2, height = 5)	
	objectColor = mc.colorSliderGrp("objectColor", parent = column2, 
	                label='Object Color', 
	                hsv=(0, 0, 0),
                    changeCommand = partial(UpdateColor),
	                columnWidth3=(70,50,80),
	                columnAlign3=("left", "left", "left"))
	
  	mc.separator(parent = column2, height = 5)
	otherConstant = mc.textField("otherConstant", 
	                parent=column2, 
	                width=200)
  	mc.separator(parent = column2, height = 5)
	mc.button(label = "Set Custom Constant", 
					parent = column2, 
					width = 120)
  	mc.separator(parent = column2, height = 5)
  	objectOpaque = mc.radioButtonGrp(parent=column2, 
  	                label="Object Opaque", 
  	                numberOfRadioButtons=2, 
  	                labelArray2=("On", "Off"),
  	                vertical=True,
  	                columnAlign2=("left", "left"),
  	                width=200)
  	
  	mc.separator(parent = column2, height = 5)
  	objectMatte = mc.radioButtonGrp(parent=column2, 
  	                label="Object Matte", 
  	                numberOfRadioButtons=2, 
  	                labelArray2=("On", "Off"),
  	                vertical=True,
  	                columnAlign2=("left", "left"),
  	                width=200)
  	                
  	#Subdivide Stats
  	mc.separator(parent = column2, height = 10)
	
	mc.text("Subdivide Stats", parent=column2, enable=False)
	mc.separator(parent = column2, height = 10)
	
	mc.optionMenu(parent=column2, label="SubDiv Type")
	mc.menuItem(label="none")
	mc.menuItem(label="catclark")
	mc.menuItem(label="linear")
	
	mc.separator(parent = column2, height = 5)
	mc.intSliderGrp(parent=column2,
                	field=True,
	                label="Iteration", 
	                minValue=0, 
	                value=1,
	                columnWidth3=(50,30,120),
	                columnAttach3=("left", "left", "left"),
	                columnOffset3=(-1,0,0))
	                
	mc.separator(parent = column2, height = 5)
	mc.optionMenu(parent=column2, label="UV Smoothing")
	mc.menuItem(label="pin_corners")
	mc.menuItem(label="pin_borders")
	mc.menuItem(label="linear")
	mc.menuItem(label="smooth")

	mc.showWindow(winID)