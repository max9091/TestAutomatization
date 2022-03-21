# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 14:58:20 2016
Python 2.7
@author: max9091

ZetCode Tkinter tutorial

In this script, we use the pack manager
to create a more complex layout.

Author: Jan Bodnar
Last modified: December 2015
Website: www.zetcode.com
"""

import os
#import shutil
import codecs
import sys

import sharedFunctions as mySF

from Tkinter import X, Y, LEFT, RIGHT, TOP, BOTTOM, W, END, Text
from ttk import Frame, Label, Entry, Button

import Tkinter as tk
#import Tkconstants
import tkFileDialog
import tkMessageBox
from tkSimpleDialog import askstring

import datetime

root = tk.Tk()

root.geometry("950x520+100+100")
root.title("Write Data to ReadMe-File")
#root.iconbitmap("Iconshock-Folder-Gallery.ico")

versuch = tk.StringVar()
versuch.set("") # default value
versuchOPTIONS = tk.StringVar()
#versuchOPTIONS.set('1Versuch')

chosenDir = tk.StringVar()
readMeFilePath = tk.StringVar()
existingSpecimensStr = tk.StringVar()
existingSpecimensStr.set("")


templatePath = tk.StringVar()
templatePath.set('C:'+os.path.sep+'TestAutomatization')

#redirect all prints to log-file
originalStd = sys.stdout
sys.stdout = open(os.path.join(templatePath.get(),'writeReadMeData.log'), 'a')
print '##############################################################################'
print 'Start on: '+str(datetime.datetime.now())


DATA = {} #create new Database --> actually a dictionary

LABEL_WIDTH = 12

        
#def writeToReadMeFile(val):
#    print "Button"
#    print val

def enableWidget(child):
    try:
        child.configure(state='normal')
    except tk.TclError:
        print('WARNING: The instance <' + child.winfo_class() + '> could not be enabled')

def disableWidget(child):
    try:
        child.configure(state='disable')
    except tk.TclError:
        print('WARNING: The instance <' + child.winfo_class() + '> could not be disabled')
                  
def enableStackedFrame(frame):
    for child in frame.winfo_children():
#        print str(child.winfo_class())
        if str(child.winfo_class()) == 'TFrame': 
            enableStackedFrame(child)
        else:
            enableWidget(child)

def disableStackedFrame(frame):
#    print(str(frame.winfo_class()))
    for child in frame.winfo_children():
#        print(str(child.winfo_class()))
        if str(child.winfo_class()) == 'TFrame': 
            disableStackedFrame(child)
        else:
            disableWidget(child)
        
def refreshVersuche():
    # Reset var and delete all old options
    versuch.set('')
    optM1a['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    new_choices = versuchOPTIONS.get().split(';')
    for choice in new_choices:
        optM1a['menu'].add_command(label=choice, command=tk._setit(versuch, choice))


def acceptEntry(entry,*keys):
    value = entry.get()
    #Check first
    
    #TODO?
    
    #Then Save to DATA
    if len(keys)==1:
        DATA[keys[0]] = value
        entry.configure(foreground='orange')
        print 'INFO: User changed entry %s to %s' %(keys[0], DATA[keys[0]])
        print '--> Push "WRITE CHANGED DATA" to save input to ReadMe-File'
    elif len(keys)==2:
        print keys[1]
        if ['T','Frame rate','F_o','F_u','f'].count(keys[1]): 
            dim = root.nametowidget(entry.winfo_parent()).winfo_children()[-1]['text']
            value = '%s %s' %(value, dim)
        DATA[keys[0]][keys[1]] = value
        entry.configure(foreground='orange')
        print 'INFO: User changed entry %s->%s to %s' %(keys[0], keys[1], DATA[keys[0]][keys[1]])
        print '--> Push "WRITE CHANGED DATA" to save input to ReadMe-File'
    else:
        print('ERROR: Given number of keys is invalid!')
        entry.configure(foreground='red')  
        
def saveBlock(dataL,block):
#    blockData = {}    
    if DATA.has_key(block) and dataL.count(str(block)+':'): 
        lineIndex = dataL.index(str(block)+':') + 1
        i = 0
        while dataL[lineIndex].startswith('\t*'):    #do as long line starts with '\t*'
            line = dataL[lineIndex][2:]
            if line.count('='):
                key = line.split('=')[0]
            else:
                key = 'key%02d' % (int(i))
            dataL[lineIndex] = '\t*'+key+'= '+DATA[block][key]
            lineIndex += 1
            i += 1
    else:
        print("WARNING: Block doesn't exist")
        
    return dataL


def writeToReadMeFile():
#    with codecs.open(readMeFilePath.get(),'r','utf-8') as f:
    with codecs.open(readMeFilePath.get(),'r',encoding='utf-8') as f:
        dataLines = f.read().splitlines()
    
    #search for correct line
    run = entry1c.get()
    runStartIndex, runEndIndex = getRunIndices(int(run),dataLines)
    
    #replace line with new input in dataLines
    dataLines[runStartIndex+1] = DATA['StartTime'] + ' - ' + DATA['EndTime']
    dataLines[runStartIndex:runEndIndex] = saveBlock(dataLines[runStartIndex:runEndIndex],'Camera')
    dataLines[runStartIndex:runEndIndex] = saveBlock(dataLines[runStartIndex:runEndIndex],'RT')
    dataLines[runStartIndex:runEndIndex] = saveBlock(dataLines[runStartIndex:runEndIndex],'Loading')
    dataLines[runStartIndex:runEndIndex] = saveBlock(dataLines[runStartIndex:runEndIndex],'Results')
    
    #write all dataLines to file
    i=0
#    with codecs.open(readMeFilePath.get(),'w','utf-8') as f:
    with codecs.open(readMeFilePath.get(),'w',encoding='utf-8') as f:
        for line in dataLines:
            f.write(line)
            i+=1
            if not i==len(dataLines): f.write('\n')
    
    print 'INFO: User Input saved to %s' %(readMeFilePath.get().split(os.sep)[-1])
    
    showReadMeFile()
    
    #recolor entries to green
    for frame in frameLeft.winfo_children(): 
        for child in frame.winfo_children():
            if str(child.winfo_class()) == 'TEntry' and str(child['foreground']) == 'green':
                child.configure(foreground='')
            if str(child.winfo_class()) == 'TEntry' and str(child['foreground']) == 'orange':
                child.configure(foreground='green')
    
    enableStackedFrame(frame1d)
    disableWidget(B1e)
    enableStackedFrame(frame1c)

def deleteEntryOfFrame(parentFrame):
    for frame in parentFrame.winfo_children(): #delete text in entries 
        for child in frame.winfo_children():
            if str(child.winfo_class()) == 'TEntry':
                child.delete(0,END)
                child.configure(foreground='')
    
    for frame in parentFrame.winfo_children(): #Delete Units
        if len(frame.winfo_children())>2:
            frame.winfo_children()[-1].destroy()
  

def resetGUI():
    global DATA
    DATA = {}
    deleteEntryOfFrame(frameLeft)
    
    txt1.configure(state='normal')
    txt1.delete(1.0,END)
    txt1.configure(state='disable')
    disableStackedFrame(frameTop2)
    disableStackedFrame(frameLeft)
    disableStackedFrame(frameRight)
    


def CreateDir():
    resetGUI()
#    myDir = 'I:/institut/PROJEKTE/2015_01_Aerostruts/03_TECHNIK/03_Experiment/_TESTS_'
#    myDir = 'E:\\wdPython\\TestAssembly'
    myDir = os.getcwd()
    tempdir = tkFileDialog.askdirectory(parent=root, initialdir= myDir, title='Please select a parent directory')
    tempdir = tempdir.replace('/','\\')
        
    if os.path.isdir(tempdir):
        newAssyName = askstring("New TestAssy", "Choose name for new TestAssy?")
        chosenDir.set(os.path.join(tempdir,newAssyName))
        os.mkdir(chosenDir.get())
        os.chdir(chosenDir.get())
        #Make subdirectories
        os.mkdir('_TestAnalysis')
        os.mkdir(os.path.join('_TestAnalysis','archive'))
        os.mkdir(os.path.join('_TestAnalysis','plots'))
        os.mkdir('StatischeVersuche')
        os.mkdir(os.path.join('StatischeVersuche','cubusData'))
        os.mkdir('ZyklischeVersuche')
        
        print 'INFO: User chose %s as working directory' %chosenDir.get()
        versuchOPTIONS.set(';'.join(mySF.getVersuche(chosenDir.get())))
        refreshVersuche()
        enableStackedFrame(frame0)
        disableWidget(buttonGetPrevRun)
        enableStackedFrame(frame1a)


def ChooseDir():
    resetGUI()
#    myDir = 'I:/institut/PROJEKTE/2015_01_Aerostruts/03_TECHNIK/03_Experiment/_TESTS_'
#    myDir = 'E:\\wdPython\\TestAssembly'
    myDir = os.getcwd()
    tempdir = tkFileDialog.askdirectory(parent=root, initialdir= myDir, title='Please select a directory')
    tempdir = tempdir.replace('/','\\')
    if os.path.isdir(tempdir):
        chosenDir.set(tempdir)
        os.chdir(tempdir)
        print 'INFO: User chose %s as working directory' % tempdir
        versuchOPTIONS.set(';'.join(mySF.getVersuche(chosenDir.get())))
        refreshVersuche()
        enableStackedFrame(frame0)
        disableWidget(buttonGetPrevRun)
        enableStackedFrame(frame1a)       


def showExistingSpecimens(path=None):
    if path==None: 
        path=os.path.join(os.getcwd(),versuch.get())
    existingSpecimens = mySF.getSpecimens(path)
    existingSpecimensStr.set(', '.join([x[-2:] for x in existingSpecimens]))


def createNewReadMeFile(specimen):
    newDir = os.path.join(chosenDir.get(),versuch.get(),specimen)
    if not os.access(newDir, os.F_OK):
        os.mkdir(newDir)
    assemblyName = chosenDir.get().split(os.sep)[-1]
    if versuch.get() == 'StatischeVersuche':
        newReadMeFilePath = os.path.join(newDir, 'ReadME_Static_'+ assemblyName + '_' + specimen + '.txt')
        testType = u'Statischer Belastungsversuch'+'\n\n'
    else:
        newReadMeFilePath = os.path.join(newDir, 'ReadME_'+ assemblyName + '_' + specimen + '.txt')
        testType = u'Zyklischer Ermüdungsversuch'+'\n\n'
    if not os.path.isfile(newReadMeFilePath): 
        with codecs.open(newReadMeFilePath,'w',encoding='utf-8') as f:
            f.write(testType)
            f.write(chosenDir.get().split(os.sep)[-1] + '\n')
            f.write(specimen + '\n')
            f.write('________________________')
        print 'INFO: ReadMe-File %s created!' %(newReadMeFilePath.split(os.sep)[-1])
        return newReadMeFilePath
    else:
        tkMessageBox.showerror('Error','No ReadMe-file created!')
        return None

def createNewRun(run):
    print 'INFO: User chose to create a new run Run%02d' %(run)
    if versuch.get() == 'StatischeVersuche':
        newTemplatePath = os.path.join(templatePath.get(),'template_newStaticRUN.txt')
    else:
        newTemplatePath = os.path.join(templatePath.get(),'template_newRUN.txt')
    with codecs.open(newTemplatePath,'r',encoding='utf-8') as f_in:
        data = f_in.read() 
    with codecs.open(readMeFilePath.get(),'a',encoding='utf-8') as f_out:
        f_out.write('\n######---Run_' + '%02d' %(run) + '---######\n')
        f_out.write(data)
       
    cubusPath = os.path.join(os.sep.join(readMeFilePath.get().split(os.sep)[:-1]), 'cubusData')
    if not os.path.exists(cubusPath):
        os.mkdir(cubusPath)
        
    folderList = ['Einspannung','ueye','Probe']
    folderInd = 1
    for folder in folderList:
        newFolder =  os.path.join(os.sep.join(readMeFilePath.get().split(os.sep)[:-1]), 'Run%02d-Fotos%02d_%s' %(run,folderInd,folder))
        if not os.access(newFolder, os.F_OK):
            os.mkdir(newFolder)
            print 'INFO: New folder with name <%s> created' %(newFolder) 
        folderInd = folderInd+1
        
        
def showReadMeFile():
    print 'INFO: Show File %s' %(readMeFilePath.get().split(os.sep)[-1])
    enableStackedFrame(frame3)
    txt1.configure(state='normal')
    txt1.configure(foreground='black')
    with codecs.open(readMeFilePath.get(),'r',encoding='utf-8') as f:
        dataLines = f.read().splitlines()
    txt1.delete(1.0,END)
    for line in dataLines:
        txt1.insert(tk.CURRENT,line)
        txt1.insert(tk.CURRENT,'\n')
    txt1.configure(state='disable')


def writeManuallyChangedReadMeFile():
    print 'INFO: Write manual input to file'
    content = txt1.get(1.0, END)
    with codecs.open(readMeFilePath.get(),'w',encoding='utf-8') as f:
        f.write(content[:-1])
    txt1.configure(foreground='green')
    txt1.configure(state='disable')
    enableStackedFrame(frame1d)
    disableWidget(B1e)
    enableStackedFrame(frame1c)


def readBlock(data,block): #returns a list of all block items without the indicator '\t*'
    blockData = {}
#    for line in data: print line
    if data.count(str(block)+':'): 
        lineIndex = data.index(str(block)+':') + 1
        i = 0
        while data[lineIndex].startswith('\t*'):    #do as long line starts with '\t*'
            line = data[lineIndex][2:]
#            print data[lineIndex]
#            blockData.append(data[lineIndex][2:])
            if line.count('='):
                key = line.split('=',1)[0]
                parameter = line.split('=',1)[1][1:]
            else:
                key = 'key%02d' % (int(i))
                parameter = line
            blockData[key] = parameter
            lineIndex += 1
            i += 1
            
    else:
        print("ERROR: Block doesn't exist")

    return blockData


def getRunIndices(run,dataLines):
    runStartIndex = dataLines.index('######---Run_' + '%02d' %(run) + '---######')
    runEndIndex = runStartIndex + dataLines[runStartIndex:].index('________________________') + 1
    
    return (runStartIndex, runEndIndex)
    

def loadDataOfReadMeFile():
    with codecs.open(readMeFilePath.get(),'r',encoding='utf-8') as f:
        dataLines = f.read().splitlines()
    run = entry1c.get()
    runsDone = len([line for line in dataLines if line.startswith('######---Run_')])
#    print runsDone
#    print run
#    for line in dataLines: print(line)
    if run.isdigit() and int(run)>0 and int(run)<100 and int(runsDone) >= int(run): #Run already existent
        run = int(run)
        print 'INFO: User chose Run%02d of %s' % (run, readMeFilePath.get().split(os.sep)[-2])
        print '--> Hit RETURN to confirm input!'
        runStartIndex, runEndIndex = getRunIndices(int(run),dataLines)
#        print (runStartIndex, runEndIndex)
        
        
        DATA['StartTime'] = dataLines[runStartIndex+1][0:16]
        DATA['EndTime'] = dataLines[runStartIndex+1][-16:]
        DATA['Camera'] = readBlock(dataLines[runStartIndex:runEndIndex],'Camera')
        DATA['RT'] = readBlock(dataLines[runStartIndex:runEndIndex],'RT')
        DATA['Loading'] = readBlock(dataLines[runStartIndex:runEndIndex],'Loading')
        DATA['Results'] = readBlock(dataLines[runStartIndex:runEndIndex],'Results')
        
        enableStackedFrame(frameLeft)
        
        entryInST.insert(END, DATA['StartTime'])
        entryInET.insert(END, DATA['EndTime'])
        entryInFR.insert(END, DATA['Camera']['Frame rate'].split()[0])
        Label(frameInFR, text=DATA['Camera']['Frame rate'].split()[1], width=3).pack(side=LEFT)
        entryInAN.insert(END, DATA['Camera']['Capture'])
        entryInRT.insert(END, DATA['RT']['T'].split()[0])
        Label(frameInRT, text=DATA['RT']['T'].split()[1], width=3).pack(side=LEFT)
        entryInZY.insert(END, DATA['Loading']['Cylinder'])
        entryInFO.insert(END, DATA['Loading']['F_o'].split()[0])
        Label(frameInFO, text=DATA['Loading']['F_o'].split()[1], width=3).pack(side=LEFT)
        entryInFU.insert(END, DATA['Loading']['F_u'].split()[0])
        Label(frameInFU, text=DATA['Loading']['F_u'].split()[1], width=3).pack(side=LEFT)
        entryInRR.insert(END, DATA['Loading']['R'])
        entryInFF.insert(END, DATA['Loading']['f'].split()[0])
        Label(frameInFF, text=DATA['Loading']['f'].split()[1], width=3).pack(side=LEFT)
        entryInNT.insert(END, DATA['Results']['N'])
        entryInNL.insert(END, DATA['Results']['@'])
    
        return True

#    elif int(runsDone) + 1 == int(run):
    else:
        if tkMessageBox.askyesno('Run does not exist!','Do you want to create a new Run?',icon='warning'):
            createNewRun(runsDone+1)
            entry1c.delete(0,END)
            entry1c.insert(END, runsDone+1)
            showReadMeFile()
            loadDataOfReadMeFile()
            return True
            
        else:
            print 'INFO: User do not want to create a new Run!'
            return False

#    else:
#        tkMessageBox.showinfo( 'ERROR', 'Given run number is invalid!\n(0 < Run No. < 100)')
#        return False

def getPreviousEntrys(curRun):
    with codecs.open(readMeFilePath.get(),'r',encoding='utf-8') as f:
        dataLines = f.read().splitlines()
    
    runStartIndexPrev, runEndIndexPrev = getRunIndices(int(curRun)-1,dataLines)
    prevCamera = readBlock(dataLines[runStartIndexPrev:runEndIndexPrev],'Camera')
    prevRT = readBlock(dataLines[runStartIndexPrev:runEndIndexPrev],'RT')
    prevLoading = readBlock(dataLines[runStartIndexPrev:runEndIndexPrev],'Loading')
    prevResults = readBlock(dataLines[runStartIndexPrev:runEndIndexPrev],'Results')
    try:
        tempRes = prevResults['N']
        if tempRes.startswith('='):
            tempRes = tempRes[1:]
        if tempRes.endswith('+'):
            tempRes = tempRes[:-1]
        tempRes = '=' + str(int(eval(tempRes))) + '+'
        prevResults['N'] = tempRes
    except SyntaxError:
        print 'ERROR: Previous run results couldn''t be evaluated!'
    
    deleteEntryOfFrame(frameLeft)
    
    entryInST.insert(END, dataLines[runStartIndexPrev+1][0:16])
    entryInET.insert(END, dataLines[runStartIndexPrev+1][-16:])
    entryInFR.insert(END, prevCamera['Frame rate'].split()[0])
    Label(frameInFR, text=prevCamera['Frame rate'].split()[1], width=3).pack(side=LEFT)
    entryInAN.insert(END, prevCamera['Capture'])
    entryInRT.insert(END, prevRT['T'].split()[0])
    Label(frameInRT, text=prevRT['T'].split()[1], width=3).pack(side=LEFT)
    entryInZY.insert(END, prevLoading['Cylinder'])
    entryInFO.insert(END, prevLoading['F_o'].split()[0])
    Label(frameInFO, text=prevLoading['F_o'].split()[1], width=3).pack(side=LEFT)
    entryInFU.insert(END, prevLoading['F_u'].split()[0])
    Label(frameInFU, text=prevLoading['F_u'].split()[1], width=3).pack(side=LEFT)
    entryInRR.insert(END, prevLoading['R'])
    entryInFF.insert(END, prevLoading['f'].split()[0])
    Label(frameInFF, text=prevLoading['f'].split()[1], width=3).pack(side=LEFT)
    entryInNT.insert(END, prevResults['N'])
    entryInNL.insert(END, prevResults['@'])
#    else:
#        tkMessageBox.showerror( 'ERROR', 'No previous run available')


def defineReadMeFile():
    spNo = entry1.get()
#    print str(val)
    if spNo.isdigit() and int(spNo)>0 and int(spNo)<100:
        chosenDirReadMe = os.path.join(chosenDir.get(),versuch.get())
        specimen = 'Probe%02d' % (int(spNo))
        if os.listdir(chosenDirReadMe).count(specimen): #chosen specimen folder exists?
            print 'INFO: User chose Probe%02d in %s' % (int(spNo), chosenDirReadMe)
            if versuch.get() == 'StatischeVersuche':
                readMeFilePath.set(os.path.join(chosenDirReadMe,specimen,'ReadME_Static_'+chosenDirReadMe.split(os.sep)[-2]+'_' + specimen + '.txt'))
            else:
                readMeFilePath.set(os.path.join(chosenDirReadMe,specimen,'ReadME_'+chosenDirReadMe.split(os.sep)[-2]+'_' + specimen + '.txt'))
            if not os.path.isfile(readMeFilePath.get()):
                createNewReadMeFile(specimen)
            showReadMeFile()
            disableStackedFrame(frame1b)
            enableStackedFrame(frame1c)
            enableStackedFrame(frame1d)
            disableWidget(B1e)
            #enableStackedFrame(frameIn2)
            #all frames
        else: 
            if tkMessageBox.askyesno('Specimen does not exist!','Do you want to create a new specimen?\n(folder + ReadMe-file)',icon='warning'):
                readMeFilePath.set(createNewReadMeFile(specimen))
                createNewRun(1)
                showReadMeFile()
                showExistingSpecimens()
                disableStackedFrame(frame1b)
                enableStackedFrame(frame1c)
                entry1c.delete(0,END)
                entry1c.insert(END, 1)
                buttonB1c()
            else:
                print 'INFO: User do not want to create a new specimen!'

    else:
        tkMessageBox.showinfo( 'ERROR', 'Given probe number is invalid!\n(0 < Probe No. < 100)')

        
#    if os.path.isfile(filepath):
#        print "file exists"

frameTop = Frame(root)
frameTop.pack(fill=X, side=TOP)

B1 = Button(frameTop, text ='New Assy?', command = CreateDir)
B1.pack(side = LEFT, padx=5, pady=5)

B2 = Button(frameTop, text ='Open existing Assy?', command = ChooseDir)
B2.pack(side = LEFT, padx=5, pady=5)

L1 = Label(frameTop, textvariable = chosenDir)
L1.pack(side = LEFT, padx=5, pady=5, fill=X)

frameTop2 = Frame(root)
frameTop2.pack(fill=X, side=TOP)

######## SET Assembly ########
frameTopLeft = Frame(frameTop2)
frameTopLeft.pack(side=LEFT) 

frame1a = Frame(frameTopLeft)
frame1a.pack(fill=X) 

def buttonB1a():
    disableStackedFrame(frame1a)
    enableStackedFrame(frame1b)
    showExistingSpecimens()

optM1a = tk.OptionMenu(frame1a, versuch, *versuchOPTIONS.get().split(';'))
optM1a.pack(side=LEFT, padx=5)

B1a = Button(frame1a, text ='Set', command = lambda: buttonB1a())
B1a.pack(side=LEFT)

######## SET Specimen ########
frame1b = Frame(frame1a)
frame1b.pack(side=LEFT)

lbl1b = Label(frame1b, text="   Specimen:")
lbl1b.pack(side=LEFT, padx=5, pady=5)           
   
entry1 = Entry(frame1b)
entry1.bind("<Return>",(lambda event: defineReadMeFile()))
entry1.pack(side=LEFT, padx=5)

E1 = Button(frame1b, text ='Set', command = defineReadMeFile)
E1.pack(side=LEFT)

######## Show Specimen Numbers ########

frame2a = Frame(frameTopLeft)
frame2a.pack(fill=X) 

lbl2a1 = Label(frame2a, text="Existing specimens:")
lbl2a1.pack(side=LEFT, padx=5, pady=5)

lbl2a2 = Label(frame2a, textvariable = existingSpecimensStr)
lbl2a2.pack(side=LEFT, padx=5, pady=5)  

######## SET RUN ########
frame1c = Frame(frameTop2)
frame1c.pack(fill=X)

lbl1c = Label(frame1c, text="1) Choose Run:")
lbl1c.pack(side=LEFT, padx=5, pady=5)        

def buttonB1c():
    deleteEntryOfFrame(frameLeft)
    if loadDataOfReadMeFile():
        disableStackedFrame(frame1c)
        disableStackedFrame(frame1d)
        txt1.configure(foreground='black')
        curRun = entry1c.get()
        if int(curRun)>1:
            enableWidget(buttonGetPrevRun)
        else:
            disableWidget(buttonGetPrevRun)
        
        
#    else:#do nothing
        
entry1c = Entry(frame1c)
entry1c.bind("<Return>",lambda event: buttonB1c())
entry1c.pack(side=LEFT, fill=X, padx=5)

B1c = Button(frame1c, text ='Set', command = buttonB1c)
B1c.pack(side=LEFT)

######## EDIT MANUALLY ########
frame1d = Frame(frameTop2)
frame1d.pack(fill=X)

lbl1c = Label(frame1d, text="or 2) ")
lbl1c.pack(side=LEFT, padx=5, pady=5)  

def buttonB1d():
    print 'INFO: User chose to edit the ReadMe-File manually'
    deleteEntryOfFrame(frameLeft)
    disableStackedFrame(frame1c)
    disableStackedFrame(frameLeft)
    disableWidget(B1d)
    tkMessageBox.showinfo( 'WARNING', 'Only change lines according to format rules!')
    showReadMeFile()
    txt1.configure(state='normal')
    txt1.configure(foreground='orange')
    enableWidget(B1e)
    
    
    
#    if loadDataOfReadMeFile():
#        disableStackedFrame(frame1c)
#    else:#do nothing

B1d = Button(frame1d, text ='Edit ReadMe-File Manually', command = buttonB1d)
B1d.pack(side=LEFT, ipadx=17)

B1e = Button(frame1d, text ='SAVE', command = writeManuallyChangedReadMeFile)
B1e.pack(side=LEFT, padx=5)


#------------------------ DATA INPUT ------------------------#

frameBottom = Frame(root)
frameBottom.pack(fill=X,side=TOP)

frameLeft = Frame(frameBottom)
frameLeft.pack(fill=Y,side=LEFT)

frameRight = Frame(frameBottom)
frameRight.pack(fill=Y,side=LEFT,padx=5)

frame0 = Frame(frameLeft)
frame0.pack(fill=X)  #fill=X ... fill horizontally

lbl0 = Label(frame0, text="Data Input")
lbl0.pack(side=LEFT, padx=5)

def buttonPrevRun():
    if tkMessageBox.askyesno('Get data of previous run?','Do you want to get the data of the previous run. Current entry data will be overwritten!',icon='warning'):
        run = entry1c.get()
        getPreviousEntrys(run)
        print 'INFO: User put the data of the previous run as new input.'
    else:
        print 'INFO: User do not want to get the previous run data.'
    

buttonGetPrevRun = Button(frame0, text ='Get previous run data', command = buttonPrevRun)
buttonGetPrevRun.pack(side=RIGHT, padx=5, pady=5)

frameInST = Frame(frameLeft)
frameInST.pack(fill=X)

Label(frameInST, text="Start Time=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)        

entryInST = Entry(frameInST)
entryInST.bind("<Return>",(lambda event: acceptEntry(entryInST,'StartTime')))
entryInST.pack(side=LEFT, fill=X, padx=5, expand=True)

frameInET = Frame(frameLeft)
frameInET.pack(fill=X)

Label(frameInET, text="End Time=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInET = Entry(frameInET)
entryInET.bind("<Return>",(lambda event: acceptEntry(entryInET,'EndTime')))
entryInET.pack(side=LEFT, fill=X, padx=5, expand=True)


frameInFR = Frame(frameLeft)
frameInFR.pack(fill=X)

Label(frameInFR, text="Frame rate=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInFR = Entry(frameInFR)
entryInFR.bind("<Return>",(lambda event: acceptEntry(entryInFR,'Camera','Frame rate')))
entryInFR.pack(side=LEFT, fill=X, padx=5, expand=True)


frameInAN = Frame(frameLeft)
frameInAN.pack(fill=X)

Label(frameInAN, text="Capture=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInAN = Entry(frameInAN)
entryInAN.bind("<Return>",(lambda event: acceptEntry(entryInAN,'Camera','Capture')))
entryInAN.pack(side=LEFT, fill=X, padx=5, expand=True)


frameInRT = Frame(frameLeft)
frameInRT.pack(fill=X)

Label(frameInRT, text="Room temp.=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInRT = Entry(frameInRT)
entryInRT.bind("<Return>",(lambda event: acceptEntry(entryInRT,'RT','T')))
entryInRT.pack(side=LEFT, fill=X, padx=5, expand=True)

frameInZY = Frame(frameLeft)
frameInZY.pack(fill=X)

Label(frameInZY, text="Cylinder=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInZY = Entry(frameInZY)
entryInZY.bind("<Return>",(lambda event: acceptEntry(entryInZY,'Loading','Cylinder')))
entryInZY.pack(side=LEFT, fill=X, padx=5, expand=True)


frameInFO = Frame(frameLeft)
frameInFO.pack(fill=X)

Label(frameInFO, text="Upper load=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInFO = Entry(frameInFO)
entryInFO.bind("<Return>",(lambda event: acceptEntry(entryInFO,'Loading','F_o')))
entryInFO.pack(side=LEFT, fill=X, padx=5, expand=True)


frameInFU = Frame(frameLeft)
frameInFU.pack(fill=X)

Label(frameInFU, text="Lower load=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInFU = Entry(frameInFU)
entryInFU.bind("<Return>",(lambda event: acceptEntry(entryInFU,'Loading','F_u')))
entryInFU.pack(side=LEFT, fill=X, padx=5, expand=True)


frameInRR = Frame(frameLeft)
frameInRR.pack(fill=X)

Label(frameInRR, text="R-ratio=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInRR = Entry(frameInRR)
entryInRR.bind("<Return>",(lambda event: acceptEntry(entryInRR,'Loading','R')))
entryInRR.pack(side=LEFT, fill=X, padx=5, expand=True)


frameInFF = Frame(frameLeft)
frameInFF.pack(fill=X)

Label(frameInFF, text="Frequency=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInFF = Entry(frameInFF)
entryInFF.bind("<Return>",(lambda event: acceptEntry(entryInFF,'Loading','f')))
entryInFF.pack(side=LEFT, fill=X, padx=5, expand=True)


frameInNT = Frame(frameLeft)
frameInNT.pack(fill=X)

Label(frameInNT, text="Total cycles=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInNT = Entry(frameInNT)
entryInNT.bind("<Return>",(lambda event: acceptEntry(entryInNT,'Results','N')))
entryInNT.pack(side=LEFT, fill=X, padx=5, expand=True)

frameInNL = Frame(frameLeft)
frameInNL.pack(fill=X)

Label(frameInNL, text="Location=", width=LABEL_WIDTH).pack(side=LEFT, padx=5, pady=5)  

entryInNL = Entry(frameInNL)
entryInNL.bind("<Return>",(lambda event: acceptEntry(entryInNL,'Results','@')))
entryInNL.pack(side=LEFT, fill=X, padx=5, expand=True)

frameInCTRL = Frame(frameLeft)
frameInCTRL.pack(fill=X)

buttonInCTRL = Button(frameInCTRL, text ='WRITE CHANGED DATA (orange input)', command = writeToReadMeFile)
buttonInCTRL.pack(side=LEFT, padx=5, pady=5, ipadx = 30)

        
#------------------------README FILE ------------------------#
frame3 = Frame(frameRight)
frame3.pack(side=TOP, fill=X, expand=True)

lbl3 = Label(frame3, text="ReadME-File Preview")
lbl3.pack(side=TOP, anchor=W)        

frame4 = Frame(frameRight)
frame4.pack(side=TOP, fill=X, expand=True)

txt1 = Text(frame4)
txt1.pack(side=LEFT, fill=Y)

stxt1 = tk.Scrollbar(frame4)
stxt1.pack(side=LEFT, fill=Y)
stxt1.config(command=txt1.yview)

txt1.config(yscrollcommand=stxt1.set)




disableStackedFrame(frameTop2)
disableStackedFrame(frameLeft)
disableStackedFrame(frameRight)
    
root.mainloop()