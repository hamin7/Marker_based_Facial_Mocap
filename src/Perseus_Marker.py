import maya.cmds as cmds
import os
import random
import pymel.core as pm
import socket
import sys
import maya.mel as mm
import csv

recstart = 0
selectedBlend = ""
dataarray = []
gnumcurrenttime = 1

"""
menulabelarr = ['Brow Left UP','Brow Left Down','Brow Right UP','Brow Right Down','Brow Centering','Brow outer left down','Brow outer right down','Eye Close Left','Eye Close Right','Mouse Open',
                'Mouse Left Smile','Mouse Right Smile','Mouse Left Spread','Mouse Right Spread','Mouse Left Frawn','Mouse Right Frawn','Mouse Left Centering','Mouse Right Centering','Cheek Left UP',
                'Cheek Right UP']
"""


# Our mel global proc.
melproc = """
global proc portData(string $arg){
    python(("portData(\\"" + $arg + "\\")"));
}
"""

mm.eval(melproc)

def edit_cell(row, column, value):
    return 1

def startrealtimeexp(*args):
    global recstart
    global recend
    #numrow = cmds.scriptTable('scrtable', query=True, rows=True)
    if len(selectedBlend) >= 0:
        if recstart == 0:
            recstart = 1
            cmds.button( 'realtimecomm' ,edit=True, label = 'Stop Real Time Expression' )
	    #Start Comm
            cmds.commandPort(name="127.0.0.1:7777", echoOutput=False, noreturn=False,prefix="portData", returnNumCommands=True)
            cmds.commandPort(name=":7777", echoOutput=False, noreturn=False,prefix="portData", returnNumCommands=True)
        else:
            recstart = 0
            cmds.button( 'realtimecomm' ,edit=True, label = 'Start Real Time Expression' )
	    #Stop Comm
            deactivateCommandPort('127.0.0.1', '7777')

def expTrackerWindow():
    if cmds.window('expTrackerWindow', exists = True):
        cmds.deleteUI('expTrackerWindow')

    #window def
    cmds.window('expTrackerWindow',widthHeight=(900,400),title='Perseus_Boy_Facial_Mocap-conelab',minimizeButton=False,maximizeButton=False,resizeToFitChildren = True, sizeable = True)
    #cmds.rowColumnLayout(numberOfColumns=3,columnWidth=[(1,300),(2,300),(3,300)],backgroundColor=[200,200,0])

    cmds.columnLayout('temp3', width=900)
    cmds.rowColumnLayout(numberOfColumns=5,columnWidth=[(1,200),(2,50),(3,200),(4,150),(5,300)])

    cmds.text( label='' )
    cmds.text( label='' )
    cmds.text( label='' )
    cmds.text( label='' )
    cmds.text( label='' )

    #cmds.button( label = 'Save preset', command = savepresetfile,backgroundColor=[0.3412,0.8196,0.7882] )
    cmds.text( label='' )
    #cmds.button( label = 'Load preset', command = loadpresetfile,backgroundColor=[0.3412,0.8196,0.7882] )
    cmds.text( label='' )
    cmds.button( 'realtimecomm', label = 'Start Real Time Expression', command = startrealtimeexp ,backgroundColor=[0.9294,0.3294,0.5216])
    
    #cmds.button(label='close', command=('cmds.deleteUI(\"' + window + '\", window=True)'), backgroundColor=[0.9294,0.3294,0.5216])

    cmds.text( label='' )
    cmds.text( label='' )
    cmds.text( label='' )
    cmds.text( label='' )
    cmds.text( label='' )

    cmds.showWindow( 'expTrackerWindow' )

expTrackerWindow()

# 0 ~ 2
PRE_name_Nose_ctrl_X = -0.167494
PRE_name_Nose_ctrl_Y = 0.411028
PRE_name_Nose_ctrl_Z = 0.021359

# 3 ~ 5
PRE_name_downLip_ctrl_X = -0.146035
PRE_name_downLip_ctrl_Y = 0.361873
PRE_name_downLip_ctrl_Z = 0.018835

# 6 ~ 8
PRE_name_l_downLip_ctrl_X = -0.139958
PRE_name_l_downLip_ctrl_Y = 0.3657
PRE_name_l_downLip_ctrl_Z = -0.001345

# 9 ~ 11
PRE_name_r_downLip_ctrl_X = -0.140767
PRE_name_r_downLip_ctrl_Y = 0.365645
PRE_name_r_downLip_ctrl_Z = 0.036381

# 12 ~ 14
PRE_name_l_up_cheek_ctrl_X = -0.143026
PRE_name_l_up_cheek_ctrl_Y = 0.40419
PRE_name_l_up_cheek_ctrl_Z = -0.025822

# 15 ~ 17
PRE_name_l_cheek_ctrl_X = -0.121044
PRE_name_l_cheek_ctrl_Y = 0.387342
PRE_name_l_cheek_ctrl_Z = -0.03962

# 18 ~ 20
PRE_name_l_Nose_ctrl_X = -0.145003
PRE_name_l_Nose_ctrl_Y = 0.401333
PRE_name_l_Nose_ctrl_Z = 0.004767

# 21 ~ 23
PRE_name_l_upCornerLip_ctrl_X = -0.13379
PRE_name_l_upCornerLip_ctrl_Y = 0.377603
PRE_name_l_upCornerLip_ctrl_Z = -0.009102

# 24 ~ 26
PRE_name_l_jaw_cheek_ctrl_X = -0.112907
PRE_name_l_jaw_cheek_ctrl_Y = 0.400494
PRE_name_l_jaw_cheek_ctrl_Z = -0.050059

# 27 ~ 29
PRE_name_l_nose_cheek_ctrl_X = -0.146252
PRE_name_l_nose_cheek_ctrl_Y = 0.424185
PRE_name_l_nose_cheek_ctrl_Z = -0.000506

# 30 ~ 32
PRE_name_r_up_cheek_ctrl_X = -0.13576
PRE_name_r_up_cheek_ctrl_Y = 0.399635
PRE_name_r_up_cheek_ctrl_Z = 0.065753

# 33 ~ 35
PRE_name_r_cheek_ctrl_X = -0.119672
PRE_name_r_cheek_ctrl_Y = 0.387673
PRE_name_r_cheek_ctrl_Z = 0.077085

# 36 ~ 38
PRE_name_r_Nose_ctrl_X = -0.143902
PRE_name_r_Nose_ctrl_Y = 0.400701
PRE_name_r_Nose_ctrl_Z = 0.036468

# 39 ~ 41
PRE_name_r_Lip_ctrl_X = -0.134883
PRE_name_r_Lip_ctrl_Y = 0.377068
PRE_name_r_Lip_ctrl_Z = 0.047297

# 42 ~ 44
PRE_name_r_jaw_cheek_ctrl_X = -0.109223
PRE_name_r_jaw_cheek_ctrl_Y = 0.404081
PRE_name_r_jaw_cheek_ctrl_Z = 0.089479

# 45 ~ 47
PRE_name_r_nose_cheek_ctrl_X = -0.142525
PRE_name_r_nose_cheek_ctrl_Y = 0.421987
PRE_name_r_nose_cheek_ctrl_Z = 0.050257

# 48 ~ 50
PRE_name_l_down_eye_border_ctrl_X = -0.143587
PRE_name_l_down_eye_border_ctrl_Y = 0.433989
PRE_name_l_down_eye_border_ctrl_Z = -0.019365

# 51 ~ 53
PRE_name_r_down_eye_border_ctrl_X = -0.139288
PRE_name_r_down_eye_border_ctrl_Y = 0.434798
PRE_name_r_down_eye_border_ctrl_Z = 0.058149

# 54 ~ 56
PRE_name_upLip_ctrl_X = -0.152267
PRE_name_upLip_ctrl_Y = 0.390458
PRE_name_upLip_ctrl_Z = 0.019759

# 57 ~ 59
PRE_name_l_upLip_ctrl_X = -0.147181
PRE_name_l_upLip_ctrl_Y = 0.387083
PRE_name_l_upLip_ctrl_Z = 0.001216

# 60 ~ 62
PRE_name_r_upLip_ctrl_X = -0.146955
PRE_name_r_upLip_ctrl_Y = 0.385898
PRE_name_r_upLip_ctrl_Z = 0.038531

def deformface():
    global dataarray
    if len(dataarray) < 0:
        # dataarray의 인자의 첫 세개는 목뼈의 x,y,z좌표 이므로 이것이 없다면 facial_mocap의 의미 없으므로 0을 리턴.
    	return 0

    #all_rows = cmds.scriptTable('scrtable', query=True, rows=True)
    global recstart
    global gnumcurrenttime
    
    global strengthX
    global strengthY
    global strengthZ
    
    strengthX = 0.1;
    strengthY = 0.1;
    strengthZ = 0.1;
    
    all_rows = 1;
    if all_rows > 0 and recstart == 1:
        ornum = 1;

        numcurrenttime = gnumcurrenttime
        #bonename = cmds.textField('HeadbonenameF', q=True, tx=True )

        # bjoint = pm.PyNode(Jaw_CTRL)
        
        # name_Nose_ctrl (dataarray[0] ~ dataarray[2])
            
        global PRE_name_Nose_ctrl_X
        global PRE_name_Nose_ctrl_Y
        global PRE_name_Nose_ctrl_Z
        
        pm.move((float(dataarray[0]) - float(PRE_name_Nose_ctrl_X)) * strengthX, (float(dataarray[1]) - float(PRE_name_Nose_ctrl_Y)) * strengthY, (float(dataarray[2]) - float(PRE_name_Nose_ctrl_Z)) * strengthZ, 'name_Nose_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_Nose_ctrl', v=float(dataarray[0]) - PRE_name_Nose_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_Nose_ctrl', v=float(dataarray[1]) - PRE_name_Nose_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_Nose_ctrl', v=float(dataarray[2]) - PRE_name_Nose_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_Nose_ctrl_X = dataarray[0]
        PRE_name_Nose_ctrl_Y = dataarray[1]
        PRE_name_Nose_ctrl_Z = dataarray[2]
        
        # name_downLip_ctrl (dataarray[3] ~ dataarray[5])
            
        global PRE_name_downLip_ctrl_X
        global PRE_name_downLip_ctrl_Y
        global PRE_name_downLip_ctrl_Z
        
        pm.move((float(dataarray[3]) - float(PRE_name_downLip_ctrl_X)) * strengthX, (float(dataarray[4]) - float(PRE_name_downLip_ctrl_Y)) * strengthY, (float(dataarray[5]) - float(PRE_name_downLip_ctrl_Z)) * strengthZ, 'name_downLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_downLip_ctrl', v=float(dataarray[3]) - PRE_name_downLip_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_downLip_ctrl', v=float(dataarray[4]) - PRE_name_downLip_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_downLip_ctrl', v=float(dataarray[5]) - PRE_name_downLip_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_downLip_ctrl_X = dataarray[3]
        PRE_name_downLip_ctrl_Y = dataarray[4]
        PRE_name_downLip_ctrl_Z = dataarray[5]
        
        # name_l_downLip_ctrl (dataarray[6] ~ dataarray[8])
        
        global PRE_name_l_downLip_ctrl_X
        global PRE_name_l_downLip_ctrl_Y
        global PRE_name_l_downLip_ctrl_Z
        
        pm.move((float(dataarray[6]) - float(PRE_name_l_downLip_ctrl_X)) * strengthX, (float(dataarray[7]) - float(PRE_name_l_downLip_ctrl_Y)) * strengthY, (float(dataarray[8]) - float(PRE_name_l_downLip_ctrl_Z)) * strengthZ, 'name_l_downLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_l_downLip_ctrl', v=float(dataarray[6]) - PRE_name_l_downLip_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_l_downLip_ctrl', v=float(dataarray[7]) - PRE_name_l_downLip_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_l_downLip_ctrl', v=float(dataarray[8]) - PRE_name_l_downLip_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_l_downLip_ctrl_X = dataarray[6]
        PRE_name_l_downLip_ctrl_Y = dataarray[7]
        PRE_name_l_downLip_ctrl_Z = dataarray[8]
        
        # name_r_downLip_ctrl (dataarray[9] ~ dataarray[11])
        
        global PRE_name_r_downLip_ctrl_X
        global PRE_name_r_downLip_ctrl_Y
        global PRE_name_r_downLip_ctrl_Z
        
        pm.move((float(dataarray[9]) - float(PRE_name_r_downLip_ctrl_X)) * strengthX, (float(dataarray[10]) - float(PRE_name_r_downLip_ctrl_Y)) * strengthY, (float(dataarray[11]) - float(PRE_name_r_downLip_ctrl_Z)) * strengthZ, 'name_r_downLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_r_downLip_ctrl', v=float(dataarray[9]) - PRE_name_r_downLip_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_r_downLip_ctrl', v=float(dataarray[10]) - PRE_name_r_downLip_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_r_downLip_ctrl', v=float(dataarray[11]) - PRE_name_r_downLip_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_r_downLip_ctrl_X = dataarray[9]
        PRE_name_r_downLip_ctrl_Y = dataarray[10]
        PRE_name_r_downLip_ctrl_Z = dataarray[11]
        
        # name_l_up_cheek_ctrl (dataarray[12] ~ dataarray[14])
        
        global PRE_name_l_up_cheek_ctrl_X
        global PRE_name_l_up_cheek_ctrl_Y
        global PRE_name_l_up_cheek_ctrl_Z
        
        pm.move((float(dataarray[12]) - float(PRE_name_l_up_cheek_ctrl_X)) * strengthX, (float(dataarray[13]) - float(PRE_name_l_up_cheek_ctrl_Y)) * strengthY, (float(dataarray[14]) - float(PRE_name_l_up_cheek_ctrl_Z)) * strengthZ, 'name_l_up_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_l_up_cheek_ctrl', v=float(dataarray[12]) - PRE_name_l_up_cheek_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_l_up_cheek_ctrl', v=float(dataarray[13]) - PRE_name_l_up_cheek_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_l_up_cheek_ctrl', v=float(dataarray[14]) - PRE_name_l_up_cheek_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_l_up_cheek_ctrl_X = dataarray[12]
        PRE_name_l_up_cheek_ctrl_Y = dataarray[13]
        PRE_name_l_up_cheek_ctrl_Z = dataarray[14]
        
        # name_l_cheek_ctrl (dataarray[15] ~ dataarray[17])
        
        global PRE_name_l_cheek_ctrl_X
        global PRE_name_l_cheek_ctrl_Y
        global PRE_name_l_cheek_ctrl_Z
        
        pm.move((float(dataarray[15]) - float(PRE_name_l_cheek_ctrl_X)) * strengthX, (float(dataarray[16]) - float(PRE_name_l_cheek_ctrl_Y)) * strengthY, (float(dataarray[17]) - float(PRE_name_l_cheek_ctrl_Z)) * strengthZ, 'name_l_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_l_cheek_ctrl', v=float(dataarray[15]) - PRE_name_l_cheek_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_l_cheek_ctrl', v=float(dataarray[16]) - PRE_name_l_cheek_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_l_cheek_ctrl', v=float(dataarray[17]) - PRE_name_l_cheek_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])
        
        PRE_name_l_cheek_ctrl_X = dataarray[15]
        PRE_name_l_cheek_ctrl_Y = dataarray[16]
        PRE_name_l_cheek_ctrl_Z = dataarray[17]
        
        # name_l_Nose_ctrl (dataarray[18] ~ dataarray[20])
        
        global PRE_name_l_Nose_ctrl_X
        global PRE_name_l_Nose_ctrl_Y
        global PRE_name_l_Nose_ctrl_Z
        
        pm.move((float(dataarray[18]) - float(PRE_name_l_Nose_ctrl_X)) * strengthX, (float(dataarray[19]) - float(PRE_name_l_Nose_ctrl_Y)) * strengthY, (float(dataarray[20]) - float(PRE_name_l_Nose_ctrl_Z)) * strengthZ, 'name_l_Nose_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_l_Nose_ctrl', v=float(dataarray[18]) - PRE_name_l_Nose_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_l_Nose_ctrl', v=float(dataarray[19]) - PRE_name_l_Nose_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_l_Nose_ctrl', v=float(dataarray[20]) - PRE_name_l_Nose_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_l_Nose_ctrl_X = dataarray[18]
        PRE_name_l_Nose_ctrl_Y = dataarray[19]
        PRE_name_l_Nose_ctrl_Z = dataarray[20]
        
        # name_l_upCornerLip_ctrl (dataarray[21] ~ dataarray[23])
        
        global PRE_name_l_upCornerLip_ctrl_X
        global PRE_name_l_upCornerLip_ctrl_Y
        global PRE_name_l_upCornerLip_ctrl_Z
        
        pm.move((float(dataarray[21]) - float(PRE_name_l_upCornerLip_ctrl_X)) * strengthX, (float(dataarray[22]) - float(PRE_name_l_upCornerLip_ctrl_Y)) * strengthY, (float(dataarray[23]) - float(PRE_name_l_upCornerLip_ctrl_Z)) * strengthZ, 'name_l_upCornerLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_l_upCornerLip_ctrl', v=float(dataarray[21]) - PRE_name_l_upCornerLip_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_l_upCornerLip_ctrl', v=float(dataarray[22]) - PRE_name_l_upCornerLip_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_l_upCornerLip_ctrl', v=float(dataarray[23]) - PRE_name_l_upCornerLip_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_l_upCornerLip_ctrl_X = dataarray[21]
        PRE_name_l_upCornerLip_ctrl_Y = dataarray[22]
        PRE_name_l_upCornerLip_ctrl_Z = dataarray[23]
        
        # name_l_jaw_cheek_ctrl (dataarray[24] ~ dataarray[26])
        
        global PRE_name_l_jaw_cheek_ctrl_X
        global PRE_name_l_jaw_cheek_ctrl_Y
        global PRE_name_l_jaw_cheek_ctrl_Z

        pm.move((float(dataarray[24]) - float(PRE_name_l_jaw_cheek_ctrl_X)) * strengthX, (float(dataarray[25]) - float(PRE_name_l_jaw_cheek_ctrl_Y)) * strengthY, (float(dataarray[26]) - float(PRE_name_l_jaw_cheek_ctrl_Z)) * strengthZ, 'name_l_jaw_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_l_jaw_cheek_ctrl', v=float(dataarray[24]) - PRE_name_l_jaw_cheek_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_l_jaw_cheek_ctrl', v=float(dataarray[25]) - PRE_name_l_jaw_cheek_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_l_jaw_cheek_ctrl', v=float(dataarray[26]) - PRE_name_l_jaw_cheek_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_l_jaw_cheek_ctrl_X = dataarray[24]
        PRE_name_l_jaw_cheek_ctrl_Y = dataarray[25]
        PRE_name_l_jaw_cheek_ctrl_Z = dataarray[26]
        
        # name_l_nose_cheek_ctrl (dataarray[27] ~ dataarray[29])
        
        global PRE_name_l_nose_cheek_ctrl_X
        global PRE_name_l_nose_cheek_ctrl_Y
        global PRE_name_l_nose_cheek_ctrl_Z
        
        pm.move((float(dataarray[27]) - float(PRE_name_l_nose_cheek_ctrl_X)) * strengthX, (float(dataarray[28]) - float(PRE_name_l_nose_cheek_ctrl_Y)) * strengthY, (float(dataarray[29]) - float(PRE_name_l_nose_cheek_ctrl_Z)) * strengthZ, 'name_l_nose_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_l_nose_cheek_ctrl', v=float(dataarray[27]) - PRE_name_l_nose_cheek_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_l_nose_cheek_ctrl', v=float(dataarray[28]) - PRE_name_l_nose_cheek_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_l_nose_cheek_ctrl', v=float(dataarray[29]) - PRE_name_l_nose_cheek_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_l_nose_cheek_ctrl_X = dataarray[27]
        PRE_name_l_nose_cheek_ctrl_Y = dataarray[28]
        PRE_name_l_nose_cheek_ctrl_Z = dataarray[29]
        
        # name_r_up_cheek_ctrl (dataarray[30] ~ dataarray[32])
        
        global PRE_name_r_up_cheek_ctrl_X
        global PRE_name_r_up_cheek_ctrl_Y
        global PRE_name_r_up_cheek_ctrl_Z
        
        pm.move((float(dataarray[30]) - float(PRE_name_r_up_cheek_ctrl_X)) * strengthX, (float(dataarray[31]) - float(PRE_name_r_up_cheek_ctrl_Y)) * strengthY, (float(dataarray[32]) - float(PRE_name_r_up_cheek_ctrl_Z)) * strengthZ, 'name_r_up_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_r_up_cheek_ctrl', v=float(dataarray[30]) - PRE_name_r_up_cheek_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_r_up_cheek_ctrl', v=float(dataarray[31]) - PRE_name_r_up_cheek_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_r_up_cheek_ctrl', v=float(dataarray[32]) - PRE_name_r_up_cheek_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_r_up_cheek_ctrl_X = dataarray[30]
        PRE_name_r_up_cheek_ctrl_Y = dataarray[31]
        PRE_name_r_up_cheek_ctrl_Z = dataarray[32]
        
        # name_r_cheek_ctrl (dataarray[33] ~ dataarray[35])
        
        global PRE_name_r_cheek_ctrl_X
        global PRE_name_r_cheek_ctrl_Y
        global PRE_name_r_cheek_ctrl_Z
        
        pm.move((float(dataarray[33]) - float(PRE_name_r_cheek_ctrl_X)) * strengthX, (float(dataarray[34]) - float(PRE_name_r_cheek_ctrl_Y)) * strengthY, (float(dataarray[35]) - float(PRE_name_r_cheek_ctrl_Z)) * strengthZ, 'name_r_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_r_cheek_ctrl', v=float(dataarray[33]) - PRE_name_r_cheek_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_r_cheek_ctrl', v=float(dataarray[34]) - PRE_name_r_cheek_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_r_cheek_ctrl', v=float(dataarray[35]) - PRE_name_r_cheek_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_r_cheek_ctrl_X = dataarray[33]
        PRE_name_r_cheek_ctrl_Y = dataarray[34]
        PRE_name_r_cheek_ctrl_Z = dataarray[35]
        
        # name_r_Nose_ctrl (dataarray[36] ~ dataarray[38])
        
        global PRE_name_r_Nose_ctrl_X
        global PRE_name_r_Nose_ctrl_Y
        global PRE_name_r_Nose_ctrl_Z
        
        pm.move((float(dataarray[36]) - float(PRE_name_r_Nose_ctrl_X)) * strengthX, (float(dataarray[37]) - float(PRE_name_r_Nose_ctrl_Y)) * strengthY, (float(dataarray[38]) - float(PRE_name_r_Nose_ctrl_Z)) * strengthZ, 'name_r_Nose_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_r_Nose_ctrl', v=float(dataarray[36]) - PRE_name_r_Nose_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_r_Nose_ctrl', v=float(dataarray[37]) - PRE_name_r_Nose_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_r_Nose_ctrl', v=float(dataarray[38]) - PRE_name_r_Nose_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_r_Nose_ctrl_X = dataarray[36]
        PRE_name_r_Nose_ctrl_Y = dataarray[37]
        PRE_name_r_Nose_ctrl_Z = dataarray[38]
        
        # name_r_Lip_ctrl (dataarray[39] ~ dataarray[41])
        
        global PRE_name_r_Lip_ctrl_X
        global PRE_name_r_Lip_ctrl_Y
        global PRE_name_r_Lip_ctrl_Z
        
        pm.move((float(dataarray[39]) - float(PRE_name_r_Lip_ctrl_X)) * strengthX, (float(dataarray[40]) - float(PRE_name_r_Lip_ctrl_Y)) * strengthY, (float(dataarray[41]) - float(PRE_name_r_Lip_ctrl_Z)) * strengthZ, 'name_r_Lip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_r_Lip_ctrl', v=float(dataarray[39]) - PRE_name_r_Lip_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_r_Lip_ctrl', v=float(dataarray[40]) - PRE_name_r_Lip_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_r_Lip_ctrl', v=float(dataarray[41]) - PRE_name_r_Lip_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_r_Lip_ctrl_X = dataarray[39]
        PRE_name_r_Lip_ctrl_Y = dataarray[40]
        PRE_name_r_Lip_ctrl_Z = dataarray[41]
        
        # name_r_jaw_cheek_ctrl (dataarray[42] ~ dataarray[44])
        
        global PRE_name_r_jaw_cheek_ctrl_X
        global PRE_name_r_jaw_cheek_ctrl_Y
        global PRE_name_r_jaw_cheek_ctrl_Z
        
        pm.move((float(dataarray[42]) - float(PRE_name_r_jaw_cheek_ctrl_X)) * strengthX, (float(dataarray[43]) - float(PRE_name_r_jaw_cheek_ctrl_Y)) * strengthY, (float(dataarray[44]) - float(PRE_name_r_jaw_cheek_ctrl_Z)) * strengthZ, 'name_r_jaw_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_r_jaw_cheek_ctrl', v=float(dataarray[42]) - PRE_name_r_jaw_cheek_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_r_jaw_cheek_ctrl', v=float(dataarray[43]) - PRE_name_r_jaw_cheek_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_r_jaw_cheek_ctrl', v=float(dataarray[44]) - PRE_name_r_jaw_cheek_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_r_jaw_cheek_ctrl_X = dataarray[42]
        PRE_name_r_jaw_cheek_ctrl_Y = dataarray[43]
        PRE_name_r_jaw_cheek_ctrl_Z = dataarray[44]
        
        # name_r_nose_cheek_ctrl (dataarray[45] ~ dataarray[47])
        
        global PRE_name_r_nose_cheek_ctrl_X
        global PRE_name_r_nose_cheek_ctrl_Y
        global PRE_name_r_nose_cheek_ctrl_Z
        
        pm.move((float(dataarray[45]) - float(PRE_name_r_nose_cheek_ctrl_X)) * strengthX, (float(dataarray[46]) - float(PRE_name_r_nose_cheek_ctrl_Y)) * strengthY, (float(dataarray[47]) - float(PRE_name_r_nose_cheek_ctrl_Z)) * strengthZ, 'name_r_nose_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_r_nose_cheek_ctrl', v=float(dataarray[45]) - PRE_name_r_nose_cheek_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_r_nose_cheek_ctrl', v=float(dataarray[46]) - PRE_name_r_nose_cheek_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_r_nose_cheek_ctrl', v=float(dataarray[47]) - PRE_name_r_nose_cheek_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_r_nose_cheek_ctrl_X = dataarray[45]
        PRE_name_r_nose_cheek_ctrl_Y = dataarray[46]
        PRE_name_r_nose_cheek_ctrl_Z = dataarray[47]
        
        # name_l_down_eye_border_ctrl (dataarray[48] ~ dataarray[50])
        
        global PRE_name_l_down_eye_border_ctrl_X
        global PRE_name_l_down_eye_border_ctrl_Y
        global PRE_name_l_down_eye_border_ctrl_Z
        
        pm.move((float(dataarray[48]) - float(PRE_name_l_down_eye_border_ctrl_X)) * strengthX, (float(dataarray[49]) - float(PRE_name_l_down_eye_border_ctrl_Y)) * strengthY, (float(dataarray[50]) - float(PRE_name_l_down_eye_border_ctrl_Z)) * strengthZ, 'name_l_down_eye_border_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_l_down_eye_border_ctrl', v=float(dataarray[48]) - PRE_name_l_down_eye_border_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_l_down_eye_border_ctrl', v=float(dataarray[49]) - PRE_name_l_down_eye_border_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_l_down_eye_border_ctrl', v=float(dataarray[50]) - PRE_name_l_down_eye_border_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_l_down_eye_border_ctrl_X = dataarray[48]
        PRE_name_l_down_eye_border_ctrl_Y = dataarray[49]
        PRE_name_l_down_eye_border_ctrl_Z = dataarray[50]
        
        # name_r_down_eye_border_ctrl (dataarray[51] ~ dataarray[53])
        
        global PRE_name_r_down_eye_border_ctrl_X
        global PRE_name_r_down_eye_border_ctrl_Y
        global PRE_name_r_down_eye_border_ctrl_Z
        
        pm.move((float(dataarray[51]) - float(PRE_name_r_down_eye_border_ctrl_X)) * strengthX, (float(dataarray[52]) - float(PRE_name_r_down_eye_border_ctrl_Y)) * strengthY, (float(dataarray[53]) - float(PRE_name_r_down_eye_border_ctrl_Z)) * strengthZ, 'name_r_down_eye_border_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_r_down_eye_border_ctrl', v=float(dataarray[51]) - PRE_name_r_down_eye_border_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_r_down_eye_border_ctrl', v=float(dataarray[52]) - PRE_name_r_down_eye_border_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_r_down_eye_border_ctrl', v=float(dataarray[53]) - PRE_name_r_down_eye_border_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_r_down_eye_border_ctrl_X = dataarray[51]
        PRE_name_r_down_eye_border_ctrl_Y = dataarray[52]
        PRE_name_r_down_eye_border_ctrl_Z = dataarray[53]
        
        # name_upLip_ctrl (dataarray[54] ~ dataarray[56])
        
        global PRE_name_upLip_ctrl_X
        global PRE_name_upLip_ctrl_Y
        global PRE_name_upLip_ctrl_Z
        
        pm.move((float(dataarray[54]) - float(PRE_name_upLip_ctrl_X)) * strengthX, (float(dataarray[55]) - float(PRE_name_upLip_ctrl_Y)) * strengthY, (float(dataarray[56]) - float(PRE_name_upLip_ctrl_Z)) * strengthZ, 'name_upLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_upLip_ctrl', v=float(dataarray[54]) - PRE_name_upLip_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_upLip_ctrl', v=float(dataarray[55]) - PRE_name_upLip_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_upLip_ctrl', v=float(dataarray[56]) - PRE_name_upLip_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_upLip_ctrl_X = dataarray[54]
        PRE_name_upLip_ctrl_Y = dataarray[55]
        PRE_name_upLip_ctrl_Z = dataarray[56]
        
        # name_l_upLip_ctrl (dataarray[57] ~ dataarray[59])
        
        global PRE_name_l_upLip_ctrl_X
        global PRE_name_l_upLip_ctrl_Y
        global PRE_name_l_upLip_ctrl_Z
        
        pm.move((float(dataarray[57]) - float(PRE_name_l_upLip_ctrl_X)) * strengthX, (float(dataarray[58]) - float(PRE_name_l_upLip_ctrl_Y)) * strengthY, (float(dataarray[59]) - float(PRE_name_l_upLip_ctrl_Z)) * strengthZ, 'name_l_upLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_l_upLip_ctrl', v=float(dataarray[57]) - PRE_name_l_upLip_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_l_upLip_ctrl', v=float(dataarray[58]) - PRE_name_l_upLip_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_l_upLip_ctrl', v=float(dataarray[59]) - PRE_name_l_upLip_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_l_upLip_ctrl_X = dataarray[57]
        PRE_name_l_upLip_ctrl_Y = dataarray[58]
        PRE_name_l_upLip_ctrl_Z = dataarray[59]
        
        # name_r_upLip_ctrl (dataarray[60] ~ dataarray[62])
        
        global PRE_name_r_upLip_ctrl_X
        global PRE_name_r_upLip_ctrl_Y
        global PRE_name_r_upLip_ctrl_Z
        
        pm.move((float(dataarray[60]) - float(PRE_name_r_upLip_ctrl_X)) * strengthX, (float(dataarray[61]) - float(PRE_name_r_upLip_ctrl_Y)) * strengthY, (float(dataarray[62]) - float(PRE_name_r_upLip_ctrl_Z)) * strengthZ, 'name_r_upLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        pm.setKeyframe('name_r_upLip_ctrl', v=float(dataarray[60]) - PRE_name_r_upLip_ctrl_X, attribute='TranslateX', t=[numcurrenttime])
        pm.setKeyframe('name_r_upLip_ctrl', v=float(dataarray[61]) - PRE_name_r_upLip_ctrl_Y, attribute='TranslateY', t=[numcurrenttime])
        pm.setKeyframe('name_r_upLip_ctrl', v=float(dataarray[62]) - PRE_name_r_upLip_ctrl_Z, attribute='TranslateZ', t=[numcurrenttime])

        PRE_name_r_upLip_ctrl_X = dataarray[60]
        PRE_name_r_upLip_ctrl_Y = dataarray[61]
        PRE_name_r_upLip_ctrl_Z = dataarray[62]
        

def portData(arg):
    """
    Read the 'serial' data passed in from the commandPort
    """
    global recend
    global dataarray

    dataarray=[]
        # 이차 배열의 첫 배열 dataarray.
    recVal = str(arg)
        # 받은 arg 스트링을 recVal에 넣음.
    strArray = recVal.split(",")
        # recVal 스트링을 , 경계로 쪼갬.
    for i in range(0,63):
        # 63가지의 데이터가 들어옴.
        dataarray.append(strArray[i])
        #print(strArray[i])
            # dataarray에 strArray[i] 첨부.
        #print(strArray[i])
    #createTimer(0.03, deformface)
    deformface()


def deactivateCommandPort(host, port):
    path = host + ":" + port
    active = cmds.commandPort(path, q=True)
    if active:
        cmds.commandPort(name=path, cl=True)
    else:
        print("%s is was not active" % path)
