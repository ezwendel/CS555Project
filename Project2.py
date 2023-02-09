# Elijah Wendel
# I pledge my honor that I have abided by the Stevens Honor System.

import re
from prettytable import PrettyTable

gedFile = open("gedcomfile.ged")
lines = gedFile.readlines()
tags0 = ["HEAD", "TRLR", "NOTE"]
tags1famId = ["FAMC", "FAMS"]
tags1indId = ["HUSB", "WIFE", "CHIL"]
tags1none = ["BIRT", "DEAT", "MARR", "DIV"]
tags2 = ["DATE"]
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

famDict = {}
indDict = {}

indTable = PrettyTable()
indTable.field_names = ["Individual Id", "Name", "Sex", "Birthday", "Death Date"]
# indTable.add_row(['Elijah Wendel', 'M', 'Feb-8-2000', 'N/A'])

# print(indTable)

for idx, line in enumerate(lines):
  line = line.strip()
  parts = line.split(" ")

  if (len(parts) >= 3):  
    if (parts[2] == "INDI"):
      num = re.findall(r'\d+', parts[1])
      if (idx + 1 < len(lines)):
        nextLine = lines[idx + 1].strip()
        nextLineParts = nextLine.split(" ")
        name = ""
        if (len(nextLineParts) == 4):
          name = nextLineParts[2] + " " + nextLineParts[3].strip("/")
        indDict[int(num[0])] = name

        sex = "N/A"
        birt = "N/A"
        deat = "N/A"

        for i in range(idx + 2, len(lines)):
          currLine = lines[i].strip()
          currLineParts = currLine.split(" ")
          level = currLineParts[0]
          tag = currLineParts[1]
          
          if (len(currLineParts) >= 3):
            arg = " ".join(currLineParts[2:]).strip()
            if (level == "0" and (currLineParts[2] == "INDI") or (currLineParts[2] == "FAM")):
              break
            if (level == "1" and tag == "SEX"):
              sex = arg
            elif (level == "1" and tag == "NAME"):
              name = arg
            elif (level == "1" and tag == "DEAT"):
              newLine = lines[i + 1].strip()
              newLineParts = newLine.split(" ")
              deat = " ".join(newLineParts[2:]).strip()
          else:
            if (level == "1" and tag == "BIRT"):
              newLine = lines[i + 1].strip()
              newLineParts = newLine.split(" ")
              birt = " ".join(newLineParts[2:]).strip()
            
        indTable.add_row([num[0], name, sex, birt, deat])
          
    elif (parts[2] == "FAM"):
      num = re.findall(r'\d+', parts[1])
      if (idx + 2 < len(lines)):
        husbLine = lines[idx + 1].strip()
        husbLineParts = husbLine.split(" ")
        husbId = re.findall(r'\d+', husbLineParts[2])

        wifeLine = lines[idx + 2].strip()
        wifeLineParts = wifeLine.split(" ")
        wifeId = re.findall(r'\d+', wifeLineParts[2])

        marr = "N/A"
        div = "N/A"
        children = []

        for i in range(idx + 2, len(lines)):
          currLine = lines[i].strip()
          currLineParts = currLine.split(" ")
          level = currLineParts[0]
          tag = currLineParts[1]
          
          if (len(currLineParts) >= 3):
            arg = " ".join(currLineParts[2:]).strip()
            if (level == "0" and (currLineParts[2] == "INDI") or (currLineParts[2] == "FAM")):
              break
            if (level == "1" and tag == "CHIL"):
              chilId = re.findall(r'\d+', arg)
              children.append(int(chilId[0]))
          else:
            if (level == "1" and tag == "MARR"):
              newLine = lines[i + 1].strip()
              newLineParts = newLine.split(" ")
              marr = " ".join(newLineParts[2:]).strip()
            elif (level == "1" and tag == "DIV"):
              newLine = lines[i + 1].strip()
              newLineParts = newLine.split(" ")
              div = " ".join(newLineParts[2:]).strip()

        famDict[int(num[0])] = (int(num[0]), int(husbId[0]), int(wifeId[0]), marr, div, children)

print(indTable)

indIds = list(indDict.keys())
indIds.sort()
sortedIndDict = {i: indDict[i] for i in indIds}

familyIds = list(famDict.keys())
familyIds.sort()
sortedFamDict = {i: famDict[i] for i in familyIds}

famTable = PrettyTable()
famTable.field_names = ["Family Id", "Husband", "Wife", "Marriage Date", "Divorce Date", "Children"]

for fam in sortedFamDict.keys():
  id, husb, wife, marr, div, children = sortedFamDict[fam]

  husb = indDict[husb]
  wife = indDict[wife]
  chil = []

  for child in children:
    chil.append(indDict[child])

  famTable.add_row([id, husb, wife, marr, div, chil])

print(famTable)

with open('output.txt', 'w') as out:
  out.write(str(indTable))
  out.write('\n')
  out.write(str(famTable))