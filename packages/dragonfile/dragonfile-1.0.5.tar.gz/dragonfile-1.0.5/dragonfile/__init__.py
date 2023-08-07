from readFile import readFile
from readFileSetPeriod import readFileSetPeriod
from readFileRename import readFileRename
from readValues import readValues
from fileToCsv import fileToCsv
from lenColumns import lenColumns

class DragonFile:
    def __init__ (self, dFile, nColumn, dSep=",", coding="utf-8", dictD={}, validate=False):
        self.dFile = dFile
        self.nColumn = nColumn
        self.dSep = dSep
        self.coding = coding
        self.dictD = dictD
        self.validate = validate
    
    def readFile(self):
        readFile(self)

    def readFileSetPeriod(self, varOp0="", varOp1="Manhã", varOp2="Tarde", varOp3="Noite", varLog0="6", varLog1="12", varLog2="18", twoColumn=False):
        readFileSetPeriod(self, varOp0="", varOp1="Manhã", varOp2="Tarde", varOp3="Noite", varLog0="6", varLog1="12", varLog2="18", twoColumn=False)

    def readFileRename(self, nameRow=[], renameRow=[], mode=False, varOp0=""):
        readFileRename(self, nameRow=[], renameRow=[], mode=False, varOp0="")
        
    def readValues(self):   
        readValues(self)

    def fileToCsv(self):
        fileToCsv(self)

    def lenColumns(self):
        lenColumns(self)