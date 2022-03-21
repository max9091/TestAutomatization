# -*- coding: utf-8 -*-
# Read Data from ReadME-files and put dem together in one .txt file (tab separated)
"""
Created on Thu Oct 06 10:34:39 2016

@author: max9091
"""

import os
import shutil
# import codecs
from datetime import datetime

from Tkinter import *
# import Tkinter
# import Tkconstants
import tkFileDialog
import tkMessageBox

from sharedFunctions import getSpecimens, copyDataFrom_RMfile_to_outputFile, \
    writeNewOutputFile

top = Tk()

chosenDir = StringVar()
filePaths = []


def ChooseDir():
    myDir = 'I:/institut/PROJEKTE/2015_01_Aerostruts/03_TECHNIK/03_Experiment/_TESTS_'
    tempdir = tkFileDialog.askdirectory(parent=top, initialdir=myDir, title='Please select a directory')
    #    tempdir = tkFileDialog.askdirectory(parent=top, initialdir= os.getcwd(), title='Please select a directory')
    if len(tempdir) > 0:
        chosenDir.set(tempdir.replace('/', os.path.sep))
        print 'You chose %s' % chosenDir.get()


def close_window():
    top.destroy()


# def getSpecimens(a_dir):
#    return [name for name in os.listdir(a_dir)
#            if os.path.isdir(os.path.join(a_dir, name)) and name.startswith('Probe')]

# def readBlock(data,block): #returns a list of all block items without the indicator '\t*'
#    blockData = []    
#    if data.count(str(block)+':'): 
#        lineIndex = data.index(str(block)+':') + 1
#        i = 0
#        while data[lineIndex].startswith('\t*'):    #do as long line starts with '\t*'
##            print data[lineIndex]
#            blockData.append(data[lineIndex][2:])
#            lineIndex += 1
#            i += 1
#
#    return blockData

# def getParameterFromBlock(block,key): #returns a tupel (float(value),str(dim)) for the key if found (if empty key (0.0,unknown)), otherwise it returns 0.0 as value and 'error' as dim
#    for x in block:
#        if x.startswith(str(key)): 
#            parameter = x[len(key)+1:].split()   #split up the string using a white-space character (space, '\t', '\n', '\r', '\f') as a delimiter
#            if key=='@':
#                value = ' '.join(parameter)
#                dim = None
#                break
#            
#            if len(parameter) == 2: 
#                value = parameter[0]
#                dim = parameter[1]
#            elif len(parameter) == 1:
#                value = parameter[0]
#                dim = '1'
#            else: 
#                value = 0.0
#                dim = u'unknown'
#            break
#    #is value and dim defined?
#    try:
#        (value,dim)
#    except NameError:
#        print 'ERROR: no Parameter with key <'+str(key)+'> found!'
#        return (0.0,'error')
#    else:
#        return (value,dim)


# def blockToOneLine(block):
#    return ','.join(block)
#
#
# def readDataFromFile(filepath):
#    with codecs.open(filepath,'r',encoding='utf-8') as f:
#        dataLines = f.read().splitlines()
#    return dataLines


# def getRunIndices(run,dataLines):
#    runStartIndex = dataLines.index('######---Run_' + '%02d' %(run) + '---######')
#    runEndIndex = runStartIndex + dataLines[runStartIndex:].index('________________________') + 1
#    
#    return (runStartIndex, runEndIndex)


# def copyDataFrom_RMfile_to_outputFile(README_filePath,OUTPUT_filePath):
#    data = readDataFromFile(README_filePath)
#    runsDone = len([line for line in data if line.startswith('######---Run_')])    
#    for runNo in range(1, runsDone+1):
#        writeParameterToFile(OUTPUT_filePath,'\n' + README_filePath[-6:-4])    #SpecimenNo.
#        runStartIndex, runEndIndex = getRunIndices(int(runNo),data)
#        writeParameterToFile(OUTPUT_filePath,str(runNo))                            #RunNo.
#        writeParameterToFile(OUTPUT_filePath,data[runStartIndex+1][0:16])      #Starttime
#        writeParameterToFile(OUTPUT_filePath,data[runStartIndex+1][-16:])      #Endtime
##       ##--READ DATA BLOCKS--##
#        blockRT = readBlock(data[runStartIndex:runEndIndex],'RT')
#        blockLoading = readBlock(data[runStartIndex:runEndIndex],'Loading')
#        blockResults = readBlock(data[runStartIndex:runEndIndex],'Results')
#        blockComments = readBlock(data[runStartIndex:runEndIndex],'Comments')
##       ##--WRITE DATA FROM BLOCKS--##
#        writeParameterToFile(OUTPUT_filePath,getParameterFromBlock(blockLoading,'F_o')[0])
#        writeParameterToFile(OUTPUT_filePath,getParameterFromBlock(blockLoading,'F_u')[0])
#        writeParameterToFile(OUTPUT_filePath,getParameterFromBlock(blockLoading,'R')[0])
#        writeParameterToFile(OUTPUT_filePath,getParameterFromBlock(blockLoading,'f')[0])
#        writeParameterToFile(OUTPUT_filePath,getParameterFromBlock(blockRT,'T')[0])
#        writeParameterToFile(OUTPUT_filePath,getParameterFromBlock(blockResults,'N')[0])
##        print getParameterFromBlock(blockResults,'@')
#        writeParameterToFile(OUTPUT_filePath,getParameterFromBlock(blockResults,'@')[0])
#        writeParameterToFile(OUTPUT_filePath,blockToOneLine(blockComments))


def collect_ReadMe_Data():
    destDir = os.path.join(chosenDir.get(), 'ZyklischeVersuche')
    #    print destDir
    if os.path.isdir(destDir):
        Specimens = getSpecimens(destDir)  # get a list of subdirectories of destDir
        AsmNr = destDir.split(os.path.sep)[
            -2]  # get the second last directory in destDir, which is the Assembly-Number z.B. 9A-B-00140-041
        ##--CREATE OUTPUT FILE--##
        OUTPUT_path = os.path.join(chosenDir.get(), '_TestAnalysis')
        if not os.access(OUTPUT_path, os.F_OK):
            os.mkdir(OUTPUT_path)
        OUTPUT_filePath = os.path.join(OUTPUT_path, 'CollectedReadMeData_' + AsmNr + '.txt')
        if os.path.exists(OUTPUT_filePath):
            if not os.access(os.path.join(OUTPUT_path, 'archive'), os.F_OK):
                os.mkdir(os.path.join(OUTPUT_path, 'archive'))
            shutil.copy(OUTPUT_filePath, os.path.join(OUTPUT_path, 'archive',
                                                      'CollectedReadMeData_' + AsmNr + '.txt' + '_' + datetime.now().strftime(
                                                          '%Y-%m-%d_%H-%M-%S')))
        writeNewOutputFile(OUTPUT_filePath)
        for specimen in Specimens:
            README_filePath = os.path.join(destDir, specimen, 'ReadME_' + AsmNr + '_' + specimen + '.txt')
            copyDataFrom_RMfile_to_outputFile(README_filePath, OUTPUT_filePath)

        filePaths.append(OUTPUT_filePath)
        if tkMessageBox.askyesno('More Data?', 'Do you want to collect result data of another assembly?',
                                 icon='question'):
            ChooseDir()
        else:
            for oneFile in filePaths:
                os.startfile(oneFile)
            close_window()
    else:
        tkMessageBox.showinfo('ERROR', 'Chosen Path is not valid!', icon='error')


# def writeNewOutputFile(filepath):
#    with codecs.open(filepath,'w',encoding='utf-8') as f:
#        f.write(u'SpecimenNo;RunNo;StartTime;EndTime;F_o;F_u;R;f;RT;Nges;FailureLoc;Comments;\n')
#        f.write(u'-;-;dd.mm.yyyy hh:mm;dd.mm.yyyy hh:mm;kN;kN;1;Hz;°C;1;-;-;')
#
#
# def writeParameterToFile(filepath,value):
#    with codecs.open(filepath,'a',encoding='utf-8') as f:
#        f.write(value+';')


def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)


B = Button(top, text='Browse', command=ChooseDir)
B.pack(side=LEFT)

E = Button(top, text='Exit', command=close_window)
E.pack(side=RIGHT)

L1 = Label(top, textvariable=chosenDir)
L1.pack(side=TOP)

B = Button(top, text='collect ReadMe Data', command=collect_ReadMe_Data)
B.pack(side=BOTTOM)

# top.update_idletasks

top.attributes("-topmost", True)
top.mainloop()





# if not os.access(destDir, os.F_OK):
#	os.mkdir(destDir)
#
# dirSrc = os.getcwd() + '/DesignVarianten_ForkEnd/'
# dv = '9F-I-14005-1'
#
# fileOut = open(destDir + '/collectedResults.txt','w')
# fileOut.write('DesignVariante;F_max_ALU;@Verschiebung;F_max_STAHL;@Verschiebung\n')
#
# for dvNum in range(1,14+1):
#	dvStr = dv + '%02d'%dvNum
#	srcFile = dirSrc + dvStr + '/Report/Report.pdf' 
#	destFile = destDir + 'Report_' + dvStr + '.pdf'
#	shutil.copyfile(srcFile, destFile)
#	
#	#
#	with open(dirSrc + dvStr +'/Report/Datenausgabe.txt','r') as f:
#		parameterInFileList = f.read().splitlines()
#	print(parameterInFileList[0])
#	fileOut.write(parameterInFileList[0]+';')
#	fileOut.write(parameterInFileList[3]+';')
#	fileOut.write(parameterInFileList[4]+';')
#	fileOut.write(parameterInFileList[6]+';')
#	fileOut.write(parameterInFileList[7]+'\n')
#	
# fileOut.close()
