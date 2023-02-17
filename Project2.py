# Elijah Wendel
# I pledge my honor that I have abided by the Stevens Honor System.

import sys
import re
from prettytable import PrettyTable
from datetime import datetime

def analyse_gedcom(name = "gedcomfile.ged"):
  gedFile = open(name)
  lines = gedFile.readlines()
  tags0 = ["HEAD", "TRLR", "NOTE"]
  tags1famId = ["FAMC", "FAMS"]
  tags1indId = ["HUSB", "WIFE", "CHIL"]
  tags1none = ["BIRT", "DEAT", "MARR", "DIV"]
  tags2 = ["DATE"]
  months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

  famDict = {}
  indDict = {}

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
          
          idEntry = (int(num[0]), idx+1)
          nameEntry = (name, idx+2)

          sex = "N/A"
          birt = "N/A"
          deat = "N/A"

          sexEntry = ("N/A", 0)
          birtEntry = ("N/A", 0)
          deatEntry = ("N/A", 0)

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
                sexEntry = (sex, i+1)
              elif (level == "1" and tag == "NAME"):
                name = arg
                nameEntry = (name, i+1)
              elif (level == "1" and tag == "DEAT"):
                newLine = lines[i + 1].strip()
                newLineParts = newLine.split(" ")
                deat = " ".join(newLineParts[2:]).strip()
                deatEntry = (deat, i+1)
            else:
              if (level == "1" and tag == "BIRT"):
                newLine = lines[i + 1].strip()
                newLineParts = newLine.split(" ")
                birt = " ".join(newLineParts[2:]).strip()
                birtEntry = (birt, i+1)

          entry = {'id': idEntry, 'name': nameEntry, 'sex': sexEntry, 'deat': deatEntry, 'birt': birtEntry}
              
          indDict[int(num[0])] = entry
            
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

          idEntry = (int(husbId[0]), idx+1)
          husbIdEntry = (int(husbId[0]), idx+2)
          wifeIdEntry = (int(wifeId[0]), idx+3)
          marrEntry = (marr, 0)
          divEntry = (div, 0)
          chilEntry = []


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
                chilEntry.append((int(chilId[0]), i+1))
            else:
              if (level == "1" and tag == "MARR"):
                newLine = lines[i + 1].strip()
                newLineParts = newLine.split(" ")
                marr = " ".join(newLineParts[2:]).strip()
                marrEntry = (marr, i+1)
              elif (level == "1" and tag == "DIV"):
                newLine = lines[i + 1].strip()
                newLineParts = newLine.split(" ")
                div = " ".join(newLineParts[2:]).strip()
                divEntry = (div, i+1)

          entry = { 'id': idEntry, 'husbId': husbIdEntry, 'wifeId': wifeIdEntry, 'marr': marrEntry, 'div': divEntry, 'chil': chilEntry }
          famDict[int(num[0])] = entry

  gedFile.close()

  return indDict, famDict

def print_ged_tables(indDict, famDict, outfile):
  indIds = list(indDict.keys())
  indIds.sort()
  sortedIndDict = {i: indDict[i] for i in indIds}

  familyIds = list(famDict.keys())
  familyIds.sort()
  sortedFamDict = {i: famDict[i] for i in familyIds}

  indTable = PrettyTable()
  indTable.field_names = ["Individual Id", "Name", "Sex", "Birthday", "Death Date"]

  famTable = PrettyTable()
  famTable.field_names = ["Family Id", "Husband", "Wife", "Marriage Date", "Divorce Date", "Children"]

  for ind in sortedIndDict.keys():
    indInfo = sortedIndDict[ind]

    id = ind
    name = indInfo['name'][0]
    sex = indInfo['sex'][0]
    birt = indInfo['birt'][0]
    deat = indInfo['deat'][0]

    indTable.add_row([id, name, sex, birt, deat])

  for fam in sortedFamDict.keys():
    famInfo = sortedFamDict[fam]

    id = fam
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]
    marr = famInfo['marr'][0]
    div = famInfo['div'][0]
    children = famInfo['chil']

    husb = indDict[husbId]['name'][0]
    wife = indDict[wifeId]['name'][0]
    chil = []


    for child in children:
      childId = child[0]
      chil.append(indDict[childId]['name'][0])

    famTable.add_row([id, husb, wife, marr, div, chil])

  print(indTable)
  print(famTable)
  
  outfile.write('Individuals\n')
  outfile.write(str(indTable))
  outfile.write('\n')
  outfile.write('Families\n')
  outfile.write(str(famTable))

def user_story_01(indDict, famDict):
  indIds = list(indDict.keys())
  indIds.sort()
  sortedIndDict = {i: indDict[i] for i in indIds}

  familyIds = list(famDict.keys())
  familyIds.sort()
  sortedFamDict = {i: famDict[i] for i in familyIds}

  current_datetime = datetime.date(datetime.now())

  error_list = []

  for indId in sortedIndDict.keys():
    indInfo = sortedIndDict[indId]

    id = indId
    name = indInfo['name'][0]
    birt = indInfo['birt']
    deat = indInfo['deat']

    if (birt[0] != "N/A"):
      birt_object = datetime.strptime(birt[0], '%d %b %Y').date()

      if (birt_object > current_datetime):
        error_list.append((birt[1], f'Error US01: Birth date of {name} is after the current date.'))

    if (deat[0] != "N/A"):
      deat_object = datetime.strptime(deat[0], '%d %b %Y').date()

      if (deat_object > current_datetime):
        error_list.append((deat[1], f'Error US01: Death date of {name} is after the current date.'))

  for famId in sortedFamDict.keys():
    famInfo = sortedFamDict[famId]

    id = famId
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]
    marr = famInfo['marr']
    div = famInfo['div']

    husb = indDict[husbId]['name'][0]
    wife = indDict[wifeId]['name'][0]

    if (marr[0] != "N/A"):
      marr_object = datetime.strptime(marr[0], '%d %b %Y').date()
      if (marr_object > current_datetime):
        error_list.append((marr[1], f'Error US01: Marriage date of {husb} and {wife} is after the current date.'))

    if (div[0] != "N/A"):
      div_object = datetime.strptime(div[0], '%d %b %Y').date()
      if (div_object > current_datetime):
        error_list.append((div[1], f'Error US01: Divorce date of {husb} and {wife} is after the current date.'))

  return error_list

def user_story_02(indDict, famDict):
  indIds = list(indDict.keys())
  indIds.sort()
  sortedIndDict = {i: indDict[i] for i in indIds}

  familyIds = list(famDict.keys())
  familyIds.sort()
  sortedFamDict = {i: famDict[i] for i in familyIds}

  current_datetime = datetime.date(datetime.now())

  error_list = []

  for famId in sortedFamDict.keys():
    famInfo = sortedFamDict[famId]

    id = famId
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]
    marr = famInfo['marr']
    div = famInfo['div']

    husbInfo = indDict[husbId]
    wifeInfo = indDict[wifeId]

    husb = indDict[husbId]['name'][0]
    wife = indDict[wifeId]['name'][0]

    if (marr[0] != "N/A"):
      marr_object = datetime.strptime(marr[0], '%d %b %Y').date()
      
      husbBirt = husbInfo['birt']
      wifeBirt = wifeInfo['birt']

      if (husbBirt[0] != "N/A"):
        birt_object = datetime.strptime(husbBirt[0], '%d %b %Y').date()

        if (birt_object > marr_object):
          error_list.append((husbBirt[1], f'Error US02: Birth date of {husb} is after the marriage date with {wife}.'))
      
      if (wifeBirt[0] != "N/A"):
        birt_object = datetime.strptime(wifeBirt[0], '%d %b %Y').date()

        if (birt_object > marr_object):
          error_list.append((wifeBirt[1], f'Error US02: Birth date of {wife} is after the marriage date with {husb}.'))
  return error_list

def user_story_05(indDict, famDict):
  indIds = list(indDict.keys())
  indIds.sort()
  sortedIndDict = {i: indDict[i] for i in indIds}

  familyIds = list(famDict.keys())
  familyIds.sort()
  sortedFamDict = {i: famDict[i] for i in familyIds}

  error_list = []

  for famId in sortedFamDict.keys():
    famInfo = sortedFamDict[famId]

    id = famId
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]
    marr = famInfo['marr']

    husbInfo = indDict[husbId]
    wifeInfo = indDict[wifeId]

    husb = indDict[husbId]['name'][0]
    wife = indDict[wifeId]['name'][0]

    if (marr[0] != "N/A"):
      marr_object = datetime.strptime(marr[0], '%d %b %Y').date()
      
      husbDeat = husbInfo['deat']
      wifeDeat = wifeInfo['deat']

      if (husbDeat[0] != "N/A"):
        deat_object = datetime.strptime(husbDeat[0], '%d %b %Y').date()

        if (deat_object < marr_object):
          error_list.append((husbDeat[1], f'Error US05: Death date of {husb} is before the marriage date with {wife}.'))
      
      if (wifeDeat[0] != "N/A"):
        deat_object = datetime.strptime(wifeDeat[0], '%d %b %Y').date()

        if (deat_object < marr_object):
          error_list.append((wifeDeat[1], f'Error US05: Death date of {wife} is before the marriage date with {husb}.'))
  return error_list

def user_story_06(indDict, famDict):
  indIds = list(indDict.keys())
  indIds.sort()
  sortedIndDict = {i: indDict[i] for i in indIds}

  familyIds = list(famDict.keys())
  familyIds.sort()
  sortedFamDict = {i: famDict[i] for i in familyIds}

  error_list = []

  for famId in sortedFamDict.keys():
    famInfo = sortedFamDict[famId]

    id = famId
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]
    div = famInfo['div']

    husbInfo = indDict[husbId]
    wifeInfo = indDict[wifeId]

    husb = indDict[husbId]['name'][0]
    wife = indDict[wifeId]['name'][0]

    if (div[0] != "N/A"):
      div_object = datetime.strptime(div[0], '%d %b %Y').date()
      
      husbDeat = husbInfo['deat']
      wifeDeat = wifeInfo['deat']

      if (husbDeat[0] != "N/A"):
        deat_object = datetime.strptime(husbDeat[0], '%d %b %Y').date()

        if (deat_object < div_object):
          error_list.append((husbDeat[1], f'Error US06: Death date of {husb} is before the divorce date with {wife}.'))
      
      if (wifeDeat[0] != "N/A"):
        deat_object = datetime.strptime(wifeDeat[0], '%d %b %Y').date()

        if (deat_object < div_object):
          error_list.append((wifeDeat[1], f'Error US06: Death date of {wife} is before the divorce date with {husb}.'))
  return error_list

def print_errors(error_list, out):
  for error in error_list:
    print(error[1])
    out.write(error[1])

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("requires an argument (filename)")

  indDict, famDict = analyse_gedcom(sys.argv[1])
  
  user_story_01_errors = user_story_01(indDict, famDict)
  print(user_story_01_errors)

  user_story_02_errors = user_story_02(indDict, famDict)
  print(user_story_02_errors)

  with open('output.txt', 'w') as out:
    print_ged_tables(indDict, famDict, out)
    print_errors(user_story_01_errors, out)
    print_errors(user_story_02_errors, out)
