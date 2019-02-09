#Kushal Das
#MASH Kenga Game

import MASH.api as mapi
import maya.cmds as cmds
import os
import sys



#function for getting the number of the block to be removed
def getBlock(*args):
    #query to get the value of the slider/number of block
    remBlock = cmds.intSliderGrp ("blockRemoval", q=1, v=1)
    #return block number so it can be called
    return remBlock

#a function to build the MASH network
def game():
    cmds.file(force=True, new=True)
    #length of playback for game
    cmds.playbackOptions( maxTime='20sec' )
    #lights
    cmds.directionalLight()
    cmds.scale ( 4.910268, 4.910268, 4.910268, r=True) 
    cmds.move ( 17.938379, 12.193473, 0 , r=True)
    cmds.rotate (  0, 98.271943, 0, r=True, os=True, fo=True)
    cmds.rotate ( -23.925408, 0, 0, r=True, os=True, fo=True)
    cmds.move ( 0, 0, -0.622877 , r=True)
    cmds.move (0, 0, -3.289271 , r=True)
    cmds.duplicate ()
    #// Result: directionalLight2 //
    cmds.move (-20.838684, 0, 0, r=True)
    cmds.rotate ( 0, 24.509822, 0 , r=True, os=True, fo=True)
    cmds.rotate ( 0, 103.346384, 0 , r=True, os=True, fo=True)
    cmds.rotate ( -44.285251, 0, 0 , r=True, os=True, fo=True)
    cmds.move (-14.586563, 0, 0 , r=True)
    cmds.move (0, 0, -5.104265 , r=True)
    cmds.move (0, 0, -4.284069 , r=True)
    cmds.pointLight()
    cmds.move (0, 0, 5.003762 , r=True)
    cmds.move ( 0, 0, 11.322471 , r=True)
    cmds.move ( 0, 0, 3.520321 , r=True)
    cmds.duplicate ()
    #// Result: pointLight2 //
    cmds.move ( 0, 0, -62.281584 , r=True)
    cmds.move ( 0, 0, 20.779332 , r=True)
    cmds.setAttr("pointLightShape1.intensity", 0.2)
    #prefix for parts
    pfx = "jenga_"
    #the jenga brick
    cmds.polyCube(d=3, h=0.5, n = pfx + "brick")
    myBlinn = cmds.shadingNode('blinn', asShader=True)
    cmds.select( pfx + "brick" )
    cmds.hyperShade( assign=myBlinn )
    cmds.select( cl=True )
    cmds.hyperShade( objects=myBlinn )
    cmds.setAttr ("blinn1.color", 0.243, 0.155, 0.101, type = "double3")
    cmds.setAttr ("blinn1.ambientColor", 1, 1, 1, type = "double3")
    # create a new MASH network with grid distribution
    mashNetwork = mapi.Network()
    mashNetwork.createNetwork(name = pfx + "tower", distributionStyle = 6, geometry = "Repro")
    #adjust the distribution
    cmds.setAttr(mashNetwork.distribute+".gridz", 1) 
    cmds.setAttr(mashNetwork.distribute+".gridx", 3) 
    cmds.setAttr(mashNetwork.distribute+".gridy", 1) 
    cmds.setAttr(mashNetwork.distribute+".gridAmplitudeZ", 0)
    cmds.setAttr(mashNetwork.distribute+".gridAmplitudeY", 0)  
    cmds.setAttr(mashNetwork.distribute+".gridAmplitudeX", 2.05)  
    # add a Replicator node
    rep = mashNetwork.addNode("MASH_Replicator")
    # add a Dyanmics node
    dyn = mashNetwork.addNode("MASH_Dynamics")
    # add a Python node
    py = mashNetwork.addNode("MASH_Python")
    #adjust the Replicator settings to make a tower
    cmds.setAttr(pfx+"tower_Replicator.replicants", 17)
    cmds.setAttr(pfx+"tower_Replicator.offsetPositionY", 0.5)
    cmds.setAttr(pfx+"tower_Replicator.offsetPositionX", 0)
    cmds.setAttr(pfx+"tower_Replicator.offsetPositionZ", 0)
    cmds.setAttr(pfx+"tower_Replicator.rotatePointsY", 1530)
    #ajust the bullet solver ground plane
    cmds.setAttr( pfx+"tower_BulletSolverShape.groundPlanePositionY", -0.25)
    #ajust the Dynamics settings
    cmds.setAttr (pfx+"tower_Dynamics.friction", 1)
    #add the python code
    cmds.polyCube(n=pfx+"test")

#function to return a string with the visibility command
#for the MASH Python node 
def visCommand(i):
    #adding to the list
    myList.append(i)
    #length of the list
    elements = len(myList)
    #putting the string together
    strCommand = "md.outVisibility"
    for item in range (len(myList)):
        itemNumber = "[" + str(myList[item]) + "]=0"
        visString = strCommand + itemNumber
        print visString
        if item < (len(myList)-1):
            strCommand = visString + "\n\nmd.outVisibility"
        else:
            strCommand = visString
    #return the string so it can be implemented as code
    return strCommand

#definition for each player turn            
def playerTurn(num):
    if num in myList:
        cmds.headsUpMessage( 'This block was already removed' )
    else:
        #call the game function to create MASH network
        game()
        #parts of the string for the MASH Python node
        endStr = "\n\nmd.setData()"
        s="import openMASH\n\nmd = openMASH.MASHData(thisNode)\n\n"
        #getting the visibility command
        strCommand=visCommand(num)
        #putting the string together
        pyStr = s + strCommand + endStr 
        #adding the code to the MASH Python node
        cmds.select(pfx+"test")
        cmds.addAttr(longName="code", dataType="string")
        cmds.connectAttr (pfx+"test.code", pfx+"tower_Python.pyScript")
        cmds.setAttr(pfx+"test.code", pyStr , type = "string")
    	cmds.hide(pfx+"test")
	    #another mash network to show number of turns
    	cmds.duplicate(pfx+"brick")
        cmds.select(pfx+"brick1")
        cmds.rotate(90,0,0)
        mashNetwork = mapi.Network()
        mashNetwork.createNetwork(name=pfx+"turns", distributionStyle=2)
        cmds.setAttr (pfx+"turns_Distribute.modelAxis", 3)
        cmds.setAttr (pfx+"turns_Distribute.pointCount", len(myList))
        transNode = mashNetwork.addNode("MASH_Dynamics")
	cmds.headsUpMessage( 'Turn #' + str(len(myList)))
	
#function to create the tower before any turns    
def gameStart(*args):
    #create the mash network
    game()
    #add the code to the MASH Python node
    cmds.select(pfx+"test")
    cmds.addAttr(longName="code", dataType="string")
    cmds.connectAttr (pfx+"test.code", pfx+"tower_Python.pyScript")
    endStr = "\n\nmd.setData()"
    s="import openMASH\n\nmd = openMASH.MASHData(thisNode)"
    pyStr = s + endStr
    cmds.setAttr(pfx+"test.code", str(pyStr) , type = "string")
    myList = []
    cmds.hide(pfx+"test")
    #new game message
    cmds.headsUpMessage( 'New Game' )
    
def UI():
    #check for window
    if cmds.window("gameUI", exists = True):
        cmds.deleteUI("gameUI")
    
    #creates the window
    window = cmds.window("gameUI", title = "MASH Kenga Game", w=300, h=230, mnb=0,mxb=0,sizeable=0)
    
    #window layout
    mainLayout = cmds.columnLayout(w=300,h=230)
    
    #create banner image
    d = cmds.internalVar(usd = 1)
    imagePath=d+"prefs/icons/mash-kenga-banner.jpg"
    cmds.image(w=300, h=100, image=imagePath)
        
    #add another row and add a gap
    cmds.separator(h=15)    
    
    #button 2 on second row
    cmds.button(label="New Game", w=300, h=25, command="gameStart()\n\nmyList=[]")
    
    #add another row and add a gap
    cmds.separator(h=15)
    
    #create an int slider
    cmds.intSliderGrp("blockRemoval", field=True, label='Block to Remove', minValue=4, maxValue=50, fieldMinValue=4, fieldMaxValue=50, value=4, columnWidth3 = (94,94,94) )
    
    #add another row and add a gap
    cmds.separator(h=15)   
         
    #button 2 on second row
    cmds.button(label="Remove Block", w=300, h=25, command="blockNum = getBlock()\n\nplayerTurn(blockNum)")
        
    #show UI window 
    cmds.showWindow(window)
#gameStart()
#changing the attribute and connecting to add python script

#prefix for the parts
pfx = "jenga_"

#delete existing parts
exists=cmds.objExists(pfx + "*")
if exists==1:
    cmds.file(force=True, new=True)
    pfx = "jenga_"

#run the UI
UI()
