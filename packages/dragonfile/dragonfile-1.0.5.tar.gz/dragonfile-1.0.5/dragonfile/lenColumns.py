import csv

def lenColumns(self):
        with open(self.dFile, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=self.dSep)
            first_row = next(reader)
            return len(first_row)