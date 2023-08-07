import csv

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