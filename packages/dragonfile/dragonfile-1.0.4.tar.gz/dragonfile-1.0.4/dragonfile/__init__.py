import csv

class DragonFile:
    def __init__ (self, dFile, nColumn, dSep=",", coding="utf-8", dictD={}, validate=False):
        self.dFile = dFile
        self.nColumn = nColumn
        self.dSep = dSep
        self.coding = coding
        self.dictD = dictD
        self.validate = validate
    
    def readFile(self):
        columns = []

        with open(self.dFile, encoding=self.coding) as file:
            reader = csv.reader(file, delimiter=self.dSep)
            header = next(reader)
            nameColumn = header[self.nColumn]

            for i, row in enumerate(reader):
                columns.append(row[self.nColumn])

        dictDaux = {nameColumn: columns}
        self.dictD.update(dictDaux)

        if self.validate == True:
            print("Termino",self.nColumn)
        
        self.nColumn += 1

        return self.dictD, self.nColumn

    def readFileSetPeriod(self, varOp0="", varOp1="Manhã", varOp2="Tarde", varOp3="Noite", varLog0="6", varLog1="12", varLog2="18", twoColumn=False):
        columns = []
        columnsTwo = []

        with open(self.dFile, encoding=self.coding) as file:
            reader = csv.reader(file, delimiter=self.dSep)
            header = next(reader)
            nameColumn = header[self.nColumn]
            extraColum = "New"+header[self.nColumn]
            
            for i, row in enumerate(reader):
                word = row[self.nColumn]

                if word != "":
                    word = int(word[0]+word[1])
                else:
                    word = varOp0

                if word != varOp0 :

                    if word > varLog0 and word <= varLog1:
                        word = varOp1

                    elif word > varLog1 and word < varLog2:
                        word = varOp2

                    else:
                        word = varOp3
                        
                else:
                    pass
                
                columns.append(word)
                columnsTwo.append(row[self.nColumn])

            if twoColumn == False:
                dictDaux = {extraColum: columns}
                self.dictD.update(dictDaux)

                if self.validate == True:
                    print("Termino",self.nColumn)

                self.nColumn += 1
            else:
                dictDaux1 = {nameColumn: columnsTwo}
                dictDaux2 = {extraColum: columns}

                dictDaux1.update(dictDaux2)
                self.dictD.update(dictDaux1)

                if self.validate == True:
                    print("Termino",self.nColumn)

                self.nColumn += 1
            
            return self.dictD, self.nColumn

    def readFileRename(self, nameRow=[], renameRow=[], mode=False, varOp0=""):
        columns = []

        with open(self.dFile, encoding=self.coding) as file:
            reader = csv.reader(file, delimiter=self.dSep)
            header = next(reader)
            nameColumn = header[self.nColumn]

            for row in reader:
                if mode == False:
                    if row[self.nColumn] in nameRow:
                        index = nameRow.index(row[self.nColumn])
                        columns.append(renameRow[index])
                    else:
                        columns.append(row[self.nColumn])
                else:
                    if row[self.nColumn] in nameRow:
                        index = nameRow.index(row[self.nColumn])
                        columns.append(renameRow[index])
                    else:
                        columns.append(varOp0)

            dictDaux = {nameColumn: columns}
            self.dictD.update(dictDaux)

            if self.validate == True:
                    print("Termino",self.nColumn)

            self.nColumn += 1

            return self.dictD, self.nColumn
        
    def readValues(self):   
        columns = []

        with open(self.dFile, encoding=self.coding) as file:
            reader = csv.reader(file, delimiter=self.dSep)
            header = next(reader)
            nameColumn = header[self.nColumn]

            for i, row in enumerate(reader):
                valor = row[self.nColumn]
                
                valor = valor.replace(".", "")
                valor = valor.replace(",", ".")
                columns.append(valor)
                        

        dictDaux = {nameColumn: columns}
        self.dictD.update(dictDaux)

        if self.validate == True:
            print("Termino",self.nColumn)
        
        self.nColumn += 1

        return self.dictD, self.nColumn

    def fileToCsv(self):
        with open(self.dFile, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.dictD.keys())
            writer.writerows(zip(*self.dictD.values()))

    def lenColumns(self):
        with open(self.dFile, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=self.dSep)
            first_row = next(reader)
            return len(first_row)
        
dragonfile = DragonFile

class dataDict(dragonfile):
    def __init__(self, dFile, nColumn, dSep=",", coding="utf-8", dictD={}, validate=False):
        super().__init__(dFile, nColumn, dSep, coding, dictD, validate)