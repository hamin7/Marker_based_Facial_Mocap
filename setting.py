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
#PRE_name_Nose_ctrl_Z = 0.0088093
PRE_name_Nose_ctrl_Y = 0.267482
PRE_name_Nose_ctrl_X = -0.36317

# 3 ~ 5
#PRE_name_downLip_ctrl_Z = 0.85043
PRE_name_downLip_ctrl_Y = 0.234867
PRE_name_downLip_ctrl_X = -0.371

# 6 ~ 8
#PRE_name_l_downLip_ctrl_Z = 0.045024
PRE_name_l_downLip_ctrl_Y = 0.177909
PRE_name_l_downLip_ctrl_X = -0.35571

# 9 ~ 11
#PRE_name_r_downLip_ctrl_Z = 0.076658
PRE_name_r_downLip_ctrl_Y = 0.186614
PRE_name_r_downLip_ctrl_X = -0.38361

# 12 ~ 14
#PRE_name_l_up_cheek_ctrl_Z = 0.119772
PRE_name_l_up_cheek_ctrl_Y = 0.185076
PRE_name_l_up_cheek_ctrl_X = -0.35978

# 15 ~ 17
#PRE_name_l_cheek_ctrl_Z = 0.075271
PRE_name_l_cheek_ctrl_Y = 0.114699
PRE_name_l_cheek_ctrl_X = -0.3695

# 18 ~ 20
#PRE_name_l_Nose_ctrl_Z = 0.145003
PRE_name_l_Nose_ctrl_Y = 0.401333
PRE_name_l_Nose_ctrl_X = 0.004767

# 21 ~ 23
#PRE_name_l_Lip_ctrl_Z = 0.13379
PRE_name_l_Lip_ctrl_Y = 0.377603
PRE_name_l_Lip_ctrl_X = -0.009102

# 24 ~ 26
#PRE_name_l_jaw_cheek_ctrl_Z = 0.112907
PRE_name_l_jaw_cheek_ctrl_Y = 0.400494
PRE_name_l_jaw_cheek_ctrl_X = -0.050059

# 27 ~ 29
#PRE_name_l_nose_cheek_ctrl_Z = 0.146252
PRE_name_l_nose_cheek_ctrl_Y = 0.424185
PRE_name_l_nose_cheek_ctrl_X = -0.000506

# 30 ~ 32
#PRE_name_r_up_cheek_ctrl_Z = 0.13576
PRE_name_r_up_cheek_ctrl_Y = 0.399635
PRE_name_r_up_cheek_ctrl_X = 0.065753

# 33 ~ 35
#PRE_name_r_cheek_ctrl_Z = 0.119672
PRE_name_r_cheek_ctrl_Y = 0.387673
PRE_name_r_cheek_ctrl_X = 0.077085

# 36 ~ 38
#PRE_name_r_Nose_ctrl_Z = 0.143902
PRE_name_r_Nose_ctrl_Y = 0.400701
PRE_name_r_Nose_ctrl_X = 0.036468

# 39 ~ 41
#PRE_name_r_Lip_ctrl_Z = 0.134883
PRE_name_r_Lip_ctrl_Y = 0.377068
PRE_name_r_Lip_ctrl_X = 0.047297

# 42 ~ 44
#PRE_name_r_jaw_cheek_ctrl_Z = 0.109223
PRE_name_r_jaw_cheek_ctrl_Y = 0.404081
PRE_name_r_jaw_cheek_ctrl_X = 0.089479

# 45 ~ 47
#PRE_name_r_nose_cheek_ctrl_Z = 0.142525
PRE_name_r_nose_cheek_ctrl_Y = 0.421987
PRE_name_r_nose_cheek_ctrl_X = 0.050257

# 48 ~ 50
#PRE_name_l_down_eye_border_ctrl_Z = 0.143587
PRE_name_l_down_eye_border_ctrl_Y = 0.433989
PRE_name_l_down_eye_border_ctrl_X = -0.019365

# 51 ~ 53
#PRE_name_r_down_eye_border_ctrl_Z = 0.139288
PRE_name_r_down_eye_border_ctrl_Y = 0.434798
PRE_name_r_down_eye_border_ctrl_X = 0.058149

# 54 ~ 56
#PRE_name_upLip_ctrl_Z = 0.152267
PRE_name_upLip_ctrl_Y = 0.390458
PRE_name_upLip_ctrl_X = 0.019759

# 57 ~ 59
#PRE_name_l_upLip_ctrl_Z = 0.147181
PRE_name_l_upLip_ctrl_Y = 0.387083
PRE_name_l_upLip_ctrl_X = 0.001216

# 60 ~ 62
#PRE_name_r_upLip_ctrl_Z = 0.146955
PRE_name_r_upLip_ctrl_Y = 0.385898
PRE_name_r_upLip_ctrl_X = 0.038531

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
    #global strengthZ
    
    strengthX = 75
    strengthY = 45
    #strengthZ = 50
    
    all_rows = 1
    if all_rows > 0 and recstart == 1:
        
        # name_Nose_ctrl (dataarray[0] ~ dataarray[2])
            
        global PRE_name_Nose_ctrl_X
        global PRE_name_Nose_ctrl_Y
        #global PRE_name_Nose_ctrl_Z
        
        pm.move((float(dataarray[2]) - float(PRE_name_Nose_ctrl_X)) * strengthX, (float(dataarray[1]) - float(PRE_name_Nose_ctrl_Y)) * strengthY, 'name_Nose_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        
        #PRE_name_Nose_ctrl_Z = -float(dataarray[0])
        PRE_name_Nose_ctrl_Y = dataarray[1]
        PRE_name_Nose_ctrl_X = dataarray[2]
        
        # name_downLip_ctrl (dataarray[3] ~ dataarray[5])
        # name_down_teeth_ctrl (dataarray[3] ~ dataarray[5])
        # name_jaw_ctrl (dataarray[3] ~ dataarray[5])
            
        global PRE_name_downLip_ctrl_X
        global PRE_name_downLip_ctrl_Y
        #global PRE_name_downLip_ctrl_Z
        
        pm.move(float((float(dataarray[5]) - float(PRE_name_downLip_ctrl_X)) * strengthX) * (-1), float((float(dataarray[4]) - float(PRE_name_downLip_ctrl_Y)) * strengthY) * (-1), 'name_downLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        # 치아는 입술보단 덜 움직이므로 x 좌표 움직임에 0.8 곱함.
        pm.move(float((float(dataarray[5]) - float(PRE_name_downLip_ctrl_X)) * strengthX) * (-0.5), float((float(dataarray[4]) - float(PRE_name_downLip_ctrl_Y)) * strengthY) * (0.8), 'name_down_teeth_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        # 턱도 아랫입술과 같이 움직임
        pm.move(float((float(dataarray[5]) - float(PRE_name_downLip_ctrl_X)) * strengthX) * (-0.5), float((float(dataarray[4]) - float(PRE_name_downLip_ctrl_Y)) * strengthY) * (0.8), 'name_jaw_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_downLip_ctrl_Z = -float(dataarray[3])
        PRE_name_downLip_ctrl_Y = dataarray[4]
        PRE_name_downLip_ctrl_X = dataarray[5]

        ############################################################################################
        # name_down_teeth_ctrl (dataarray[3] ~ dataarray[5])
            
        #global PRE_name_downLip_ctrl_X
        #global PRE_name_downLip_ctrl_Y
        #global PRE_name_downLip_ctrl_Z
        
        # 치아는 입술보단 덜 움직이므로 x 좌표 움직임에 0.7 곱함.
        #pm.move(float((float(dataarray[5]) - float(PRE_name_downLip_ctrl_X)) * strengthX) * (-0.7), float((float(dataarray[4]) - float(PRE_name_downLip_ctrl_Y)) * strengthY) * (-1), 'name_down_teeth_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_downLip_ctrl_Z = -float(dataarray[3])
        #PRE_name_downLip_ctrl_Y = dataarray[4]
        #PRE_name_downLip_ctrl_X = dataarray[5]
        ############################################################################################
        
        # name_l_downLip_ctrl (dataarray[6] ~ dataarray[8])
        
        global PRE_name_l_downLip_ctrl_X
        global PRE_name_l_downLip_ctrl_Y
        #global PRE_name_l_downLip_ctrl_Z
        
        pm.move(float((float(dataarray[8]) - float(PRE_name_l_downLip_ctrl_X)) * strengthX) * (-1), float((float(dataarray[7]) - float(PRE_name_l_downLip_ctrl_Y)) * strengthY) * (-1), 'name_l_downLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )


        #PRE_name_l_downLip_ctrl_Z = -float(dataarray[6])
        PRE_name_l_downLip_ctrl_Y = dataarray[7]
        PRE_name_l_downLip_ctrl_X = dataarray[8]
        
        # name_r_downLip_ctrl (dataarray[9] ~ dataarray[11])
        
        global PRE_name_r_downLip_ctrl_X
        global PRE_name_r_downLip_ctrl_Y
        #global PRE_name_r_downLip_ctrl_Z
        
        pm.move((float(dataarray[11]) - float(PRE_name_r_downLip_ctrl_X)) * strengthX, float((float(dataarray[10]) - float(PRE_name_r_downLip_ctrl_Y)) * strengthY) * (-1), 'name_r_downLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_r_downLip_ctrl_Z = -float(dataarray[9])
        PRE_name_r_downLip_ctrl_Y = dataarray[10]
        PRE_name_r_downLip_ctrl_X = dataarray[11]
        
        # name_l_up_cheek_ctrl (dataarray[12] ~ dataarray[14])
        
        global PRE_name_l_up_cheek_ctrl_X
        global PRE_name_l_up_cheek_ctrl_Y
        #global PRE_name_l_up_cheek_ctrl_Z
        
        pm.move((float(dataarray[14]) - float(PRE_name_l_up_cheek_ctrl_X)) * strengthX, (float(dataarray[13]) - float(PRE_name_l_up_cheek_ctrl_Y)) * strengthY, 'name_l_up_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_l_up_cheek_ctrl_Z = -float(dataarray[12])
        PRE_name_l_up_cheek_ctrl_Y = dataarray[13]
        PRE_name_l_up_cheek_ctrl_X = dataarray[14]
        
        # name_l_cheek_ctrl (dataarray[15] ~ dataarray[17])
        
        global PRE_name_l_cheek_ctrl_X
        global PRE_name_l_cheek_ctrl_Y
        #global PRE_name_l_cheek_ctrl_Z
        
        pm.move((float(dataarray[17]) - float(PRE_name_l_cheek_ctrl_X)) * strengthX, (float(dataarray[16]) - float(PRE_name_l_cheek_ctrl_Y)) * strengthY, 'name_l_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        
        #PRE_name_l_cheek_ctrl_Z = -float(dataarray[15])
        PRE_name_l_cheek_ctrl_Y = dataarray[16]
        PRE_name_l_cheek_ctrl_X = dataarray[17]
        
        # name_l_Nose_ctrl (dataarray[18] ~ dataarray[20])
        
        global PRE_name_l_Nose_ctrl_X
        global PRE_name_l_Nose_ctrl_Y
        #global PRE_name_l_Nose_ctrl_Z
        
        pm.move((float(dataarray[20]) - float(PRE_name_l_Nose_ctrl_X)) * strengthX, (float(dataarray[19]) - float(PRE_name_l_Nose_ctrl_Y)) * strengthY, 'name_l_Nose_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_l_Nose_ctrl_Z = -float(dataarray[18])
        PRE_name_l_Nose_ctrl_Y = dataarray[19]
        PRE_name_l_Nose_ctrl_X = dataarray[20]
        
        # name_l_Lip_ctrl (dataarray[21] ~ dataarray[23])
        
        global PRE_name_l_Lip_ctrl_X
        global PRE_name_l_Lip_ctrl_Y
        #global PRE_name_l_Lip_ctrl_Z
        
        pm.move(float((float(dataarray[23]) - float(PRE_name_l_Lip_ctrl_X)) * strengthX) * (-1), (float(dataarray[22]) - float(PRE_name_l_Lip_ctrl_Y)) * strengthY, 'name_l_Lip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_l_Lip_ctrl_Z = -float(dataarray[21])
        PRE_name_l_Lip_ctrl_Y = dataarray[22]
        PRE_name_l_Lip_ctrl_X = dataarray[23]
        
        # name_l_jaw_cheek_ctrl (dataarray[24] ~ dataarray[26])
        
        global PRE_name_l_jaw_cheek_ctrl_X
        global PRE_name_l_jaw_cheek_ctrl_Y
        #global PRE_name_l_jaw_cheek_ctrl_Z

        pm.move((float(dataarray[26]) - float(PRE_name_l_jaw_cheek_ctrl_X)) * strengthX, (float(dataarray[25]) - float(PRE_name_l_jaw_cheek_ctrl_Y)) * strengthY, 'name_l_jaw_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_l_jaw_cheek_ctrl_Z = -float(dataarray[24])
        PRE_name_l_jaw_cheek_ctrl_Y = dataarray[25]
        PRE_name_l_jaw_cheek_ctrl_X = dataarray[26]
        
        # name_l_nose_cheek_ctrl (dataarray[27] ~ dataarray[29])
        
        global PRE_name_l_nose_cheek_ctrl_X
        global PRE_name_l_nose_cheek_ctrl_Y
        #global PRE_name_l_nose_cheek_ctrl_Z
        
        pm.move((float(dataarray[29]) - float(PRE_name_l_nose_cheek_ctrl_X)) * strengthX, (float(dataarray[28]) - float(PRE_name_l_nose_cheek_ctrl_Y)) * strengthY, 'name_l_nose_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_l_nose_cheek_ctrl_Z = -float(dataarray[27])
        PRE_name_l_nose_cheek_ctrl_Y = dataarray[28]
        PRE_name_l_nose_cheek_ctrl_X = dataarray[29]
        
        # name_r_up_cheek_ctrl (dataarray[30] ~ dataarray[32])
        
        global PRE_name_r_up_cheek_ctrl_X
        global PRE_name_r_up_cheek_ctrl_Y
        #global PRE_name_r_up_cheek_ctrl_Z
        
        pm.move((float(dataarray[32]) - float(PRE_name_r_up_cheek_ctrl_X)) * strengthX, (float(dataarray[31]) - float(PRE_name_r_up_cheek_ctrl_Y)) * strengthY, 'name_r_up_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_r_up_cheek_ctrl_Z = -float(dataarray[30])
        PRE_name_r_up_cheek_ctrl_Y = dataarray[31]
        PRE_name_r_up_cheek_ctrl_X = dataarray[32]
        
        # name_r_cheek_ctrl (dataarray[33] ~ dataarray[35])
        
        global PRE_name_r_cheek_ctrl_X
        global PRE_name_r_cheek_ctrl_Y
        #global PRE_name_r_cheek_ctrl_Z
        
        pm.move((float(dataarray[35]) - float(PRE_name_r_cheek_ctrl_X)) * strengthX, (float(dataarray[34]) - float(PRE_name_r_cheek_ctrl_Y)) * strengthY, 'name_r_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_r_cheek_ctrl_Z = -float(dataarray[33])
        PRE_name_r_cheek_ctrl_Y = dataarray[34]
        PRE_name_r_cheek_ctrl_X = dataarray[35]
        
        # name_r_Nose_ctrl (dataarray[36] ~ dataarray[38])
        
        global PRE_name_r_Nose_ctrl_X
        global PRE_name_r_Nose_ctrl_Y
        #global PRE_name_r_Nose_ctrl_Z
        
        pm.move((float(dataarray[38]) - float(PRE_name_r_Nose_ctrl_X)) * strengthX, (float(dataarray[37]) - float(PRE_name_r_Nose_ctrl_Y)) * strengthY, 'name_r_Nose_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_r_Nose_ctrl_Z = -float(dataarray[36])
        PRE_name_r_Nose_ctrl_Y = dataarray[37]
        PRE_name_r_Nose_ctrl_X = dataarray[38]
        
        # name_r_Lip_ctrl (dataarray[39] ~ dataarray[41])
        
        global PRE_name_r_Lip_ctrl_X
        global PRE_name_r_Lip_ctrl_Y
        #global PRE_name_r_Lip_ctrl_Z
        
        pm.move((float(dataarray[41]) - float(PRE_name_r_Lip_ctrl_X)) * strengthX, (float(dataarray[40]) - float(PRE_name_r_Lip_ctrl_Y)) * strengthY, 'name_r_Lip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_r_Lip_ctrl_Z = -float(dataarray[39])
        PRE_name_r_Lip_ctrl_Y = dataarray[40]
        PRE_name_r_Lip_ctrl_X = dataarray[41]
        
        # name_r_jaw_cheek_ctrl (dataarray[42] ~ dataarray[44])
        
        global PRE_name_r_jaw_cheek_ctrl_X
        global PRE_name_r_jaw_cheek_ctrl_Y
        #global PRE_name_r_jaw_cheek_ctrl_Z
        
        pm.move((float(dataarray[44]) - float(PRE_name_r_jaw_cheek_ctrl_X)) * strengthX, (float(dataarray[43]) - float(PRE_name_r_jaw_cheek_ctrl_Y)) * strengthY, 'name_r_jaw_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_r_jaw_cheek_ctrl_Z = -float(dataarray[42])
        PRE_name_r_jaw_cheek_ctrl_Y = dataarray[43]
        PRE_name_r_jaw_cheek_ctrl_X = dataarray[44]
        
        # name_r_nose_cheek_ctrl (dataarray[45] ~ dataarray[47])
        
        global PRE_name_r_nose_cheek_ctrl_X
        global PRE_name_r_nose_cheek_ctrl_Y
        #global PRE_name_r_nose_cheek_ctrl_Z
        
        pm.move((float(dataarray[47]) - float(PRE_name_r_nose_cheek_ctrl_X)) * strengthX, (float(dataarray[46]) - float(PRE_name_r_nose_cheek_ctrl_Y)) * strengthY, 'name_r_nose_cheek_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_r_nose_cheek_ctrl_Z = -float(dataarray[45])
        PRE_name_r_nose_cheek_ctrl_Y = dataarray[46]
        PRE_name_r_nose_cheek_ctrl_X = dataarray[47]
        
        # name_l_down_eye_border_ctrl (dataarray[48] ~ dataarray[50])
        
        global PRE_name_l_down_eye_border_ctrl_X
        global PRE_name_l_down_eye_border_ctrl_Y
        #global PRE_name_l_down_eye_border_ctrl_Z
        
        pm.move((float(dataarray[50]) - float(PRE_name_l_down_eye_border_ctrl_X)) * strengthX, (float(dataarray[49]) - float(PRE_name_l_down_eye_border_ctrl_Y)) * strengthY, 'name_l_down_eye_border_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_l_down_eye_border_ctrl_Z = -float(dataarray[48])
        PRE_name_l_down_eye_border_ctrl_Y = dataarray[49]
        PRE_name_l_down_eye_border_ctrl_X = dataarray[50]
        
        # name_r_down_eye_border_ctrl (dataarray[51] ~ dataarray[53])
        
        global PRE_name_r_down_eye_border_ctrl_X
        global PRE_name_r_down_eye_border_ctrl_Y
        #global PRE_name_r_down_eye_border_ctrl_Z
        
        pm.move((float(dataarray[53]) - float(PRE_name_r_down_eye_border_ctrl_X)) * strengthX, (float(dataarray[52]) - float(PRE_name_r_down_eye_border_ctrl_Y)) * strengthY, 'name_r_down_eye_border_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_r_down_eye_border_ctrl_Z = -float(dataarray[51])
        PRE_name_r_down_eye_border_ctrl_Y = dataarray[52]
        PRE_name_r_down_eye_border_ctrl_X = dataarray[53]
        
        # name_upLip_ctrl (dataarray[54] ~ dataarray[56])
        # name_up_teeth_ctrl (dataarray[54] ~ dataarray[56])
        
        global PRE_name_upLip_ctrl_X
        global PRE_name_upLip_ctrl_Y
        #global PRE_name_upLip_ctrl_Z
        
        pm.move(float((float(dataarray[56]) - float(PRE_name_upLip_ctrl_X)) * strengthX) * (-1), (float(dataarray[55]) - float(PRE_name_upLip_ctrl_Y)) * strengthY, 'name_upLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )
        
        # 이빨은 입술보단 좌우로 덜 움직이니 x좌표 움직임에 0.5곱함.
        pm.move(float((float(dataarray[56]) - float(PRE_name_upLip_ctrl_X)) * strengthX) * (-0.5), (float(dataarray[55]) - float(PRE_name_upLip_ctrl_Y)) * strengthY, 'name_up_teeth_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_upLip_ctrl_Z = -float(dataarray[54])
        PRE_name_upLip_ctrl_Y = dataarray[55]
        PRE_name_upLip_ctrl_X = dataarray[56]

        ############################################################################################
        # name_up_teeth_ctrl (dataarray[54] ~ dataarray[56])
        
        #global PRE_name_upLip_ctrl_X
        #global PRE_name_upLip_ctrl_Y
        #global PRE_name_upLip_ctrl_Z
        
        # 이빨은 입술보단 좌우로 덜 움직이니 x좌표 움직임에 0.5곱함.
        #pm.move(float((float(dataarray[56]) - float(PRE_name_upLip_ctrl_X)) * strengthX) * (-0.5), (float(dataarray[55]) - float(PRE_name_upLip_ctrl_Y)) * strengthY, 'name_up_teeth_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_upLip_ctrl_Z = -float(dataarray[54])
        #PRE_name_upLip_ctrl_Y = dataarray[55]
        #PRE_name_upLip_ctrl_X = dataarray[56]
        ############################################################################################
        
        # name_l_upLip_ctrl (dataarray[57] ~ dataarray[59])
        
        global PRE_name_l_upLip_ctrl_X
        global PRE_name_l_upLip_ctrl_Y
        #global PRE_name_l_upLip_ctrl_Z
        
        pm.move(float((float(dataarray[59]) - float(PRE_name_l_upLip_ctrl_X)) * strengthX) * (-1), (float(dataarray[58]) - float(PRE_name_l_upLip_ctrl_Y)) * strengthY, 'name_l_upLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_l_upLip_ctrl_Z = -float(dataarray[57])
        PRE_name_l_upLip_ctrl_Y = dataarray[58]
        PRE_name_l_upLip_ctrl_X = dataarray[59]
        
        # name_r_upLip_ctrl (dataarray[60] ~ dataarray[62])
        
        global PRE_name_r_upLip_ctrl_X
        global PRE_name_r_upLip_ctrl_Y
        #global PRE_name_r_upLip_ctrl_Z
        
        pm.move((float(dataarray[62]) - float(PRE_name_r_upLip_ctrl_X)) * strengthX, (float(dataarray[61]) - float(PRE_name_r_upLip_ctrl_Y)) * strengthY, 'name_r_upLip_ctrl', relative=True, objectSpace=True, worldSpaceDistance=True )

        #PRE_name_r_upLip_ctrl_Z = -float(dataarray[60])
        PRE_name_r_upLip_ctrl_Y = dataarray[61]
        PRE_name_r_upLip_ctrl_X = dataarray[62]
        

def portData(arg):
    """
    Read the 'serial' data passed in from the commandPort
    """
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
