import csv

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