# -*- coding: utf-8 -*-
# -*- Python 3 -*-
# Read Data from ReadME-files and put dem together in one .txt file (tab separated)
"""
Created on Thu Oct 06 10:34:39 2016

@author: max9091
"""

import os
import shutil
#import codecs
import sys
from datetime import datetime

from sharedFunctions import getSpecimens, copyDataFrom_RMfile_to_outputFile, \
    writeNewOutputFile, writeNewTeXFile, copyDataFrom_RMfile_to_TeX_File, finishTeXFile
#from collectReadMeData import getSpecimens, readBlock, getParameterFromBlock, \
#    blockToOneLine, readDataFromFile, getRunIndices, copyDataFrom_RMfile_to_outputFile, \
#    writeNewOutputFile, writeParameterToFile
#from collectReadMeData import collect_ReadMe_Data
  
    
def collect_ReadMe_Data_TeX(myDir,collectComments = False):
    destDir = os.path.join(myDir,'ZyklischeVersuche')
    Specimens = getSpecimens(destDir)   #get a list of subdirectories of destDir
    AsmNr = destDir.split(os.path.sep)[-2]  #get the second last directory in destDir, which is the Assembly-Number z.B. 9A-B-00140-041
    ##--CREATE OUTPUT FILE--##
    OUTPUT_path = os.path.join(myDir,'_TestAnalysis')
    if not os.access(OUTPUT_path, os.F_OK):
        os.mkdir(OUTPUT_path)
#    OUTPUT_filePath = os.path.join(OUTPUT_path,'CollectedReadMeData_' + AsmNr + '.txt')
    TeX_filePath = os.path.join(OUTPUT_path,'CollectedReadMeData_' + AsmNr + '_TEX.tex')
    if os.path.exists(TeX_filePath):
        if not os.access(os.path.join(OUTPUT_path,'archive'), os.F_OK):
            os.mkdir(os.path.join(OUTPUT_path,'archive'))
        shutil.copy(TeX_filePath, os.path.join(OUTPUT_path,'archive','CollectedReadMeData_' + AsmNr + '_TEX.tex' + '_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
    writeNewTeXFile(TeX_filePath,AsmNr,collectComments)
    allCommentStrs = {}
    for specimen in Specimens:
        README_filePath = os.path.join(destDir,specimen,'ReadME_' + AsmNr + '_' + specimen + '.txt')     
        if collectComments:
            copyDataFrom_RMfile_to_TeX_File(README_filePath,TeX_filePath,allCommentStrs = allCommentStrs)
        else:
            copyDataFrom_RMfile_to_TeX_File(README_filePath,TeX_filePath,allCommentStrs = None)
    finishTeXFile(TeX_filePath,AsmNr,allComments = allCommentStrs)

#def writeNewOutputFile(filepath):
#    with codecs.open(filepath,'w',encoding='utf-8') as f:
#        f.write(u'SpecimenNo;RunNo;StartTime;EndTime;F_o;F_u;R;f;RT;Nges;FailureLoc;Comments;\n')
#        f.write(u'-;-;dd.mm.yyyy hh:mm;dd.mm.yyyy hh:mm;kN;kN;1;Hz;°C;1;-;-;')
#
#
#def writeParameterToFile(filepath,value):
#    with codecs.open(filepath,'a',encoding='utf-8') as f:
#        f.write(value+';')

#if __name__ == '__main__':
#    myDir = 'i:\\institut\\PROJEKTE\\2019_00_KleinProjekte\\01_RoRa_FatigueTest\\03_Technik\\9F-B-00218-0233_Alunna'
#    collect_ReadMe_Data_TeX(myDir,collectComments = True)
#
    
if len(sys.argv)>1:
    myDir = str(sys.argv[1])
    collectComments = False
    if len(sys.argv)>2:
        collectComments = str(sys.argv[2])
        if collectComments == 'collectComments':
            collectComments = True
    if os.path.isdir(myDir):
        collect_ReadMe_Data_TeX(myDir,collectComments)
    else:
         print 'The input path: <%s> does not exist!' %(myDir)
else:
    print 'Too few input arguments'
