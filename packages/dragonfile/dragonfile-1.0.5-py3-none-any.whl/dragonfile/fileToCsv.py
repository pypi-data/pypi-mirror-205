import csv

def fileToCsv(self):
        with open(self.dFile, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.dictD.keys())
            writer.writerows(zip(*self.dictD.values()))