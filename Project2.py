# Elijah Wendel
# Kshitij Gugale
# I pledge my honor that I have abided by the Stevens Honor System.

import sys
import re
from prettytable import PrettyTable
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_sorted_dicts(indDict, famDict):
  indIds = list(indDict.keys())
  indIds.sort()
  sortedIndDict = {i: indDict[i] for i in indIds}

  familyIds = list(famDict.keys())
  familyIds.sort()
  sortedFamDict = {i: famDict[i] for i in familyIds}

  return sortedIndDict, sortedFamDict

def get_age_at_time(birth_date, time_to_compare):
  return time_to_compare.year - birth_date.year - ((time_to_compare.month, time_to_compare.day) < (birth_date.month, birth_date.day))

def birth_before_death(indDict):
    error_list = []

    for id, entry in indDict.items():
        birt_date = entry['birt'][0]
        deat_date = entry['deat'][0]
        
        if birt_date != "N/A" and deat_date != "N/A":
            birt = datetime.strptime(birt_date, '%d %b %Y')
            deat = datetime.strptime(deat_date, '%d %b %Y')
            
            if birt > deat:
                error_list.append(( entry['birt'][1], f"ERROR US03: Individual {id} has birth date ({birt_date}) after death date ({deat_date})."))
    
    return error_list


def marriage_before_divorce(famDict):
    error_list = []

    for id, entry in famDict.items():
        marr_date = entry['marr'][0]
        div_date = entry['div'][0]
        
        if marr_date != "N/A" and div_date != "N/A":
            marr = datetime.strptime(marr_date, '%d %b %Y')
            div = datetime.strptime(div_date, '%d %b %Y')
            
            if marr > div:
                error_list.append(( entry['marr'][1], f"ERROR US04: Family {id} has marriage date ({marr_date}) after divorce date ({div_date})."))
    
    return error_list

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

  print('Individuals')
  print(indTable)
  print('Families')
  print(famTable)
  
  outfile.write('Individuals\n')
  outfile.write(str(indTable))
  outfile.write('\n')
  outfile.write('Families\n')
  outfile.write(str(famTable))

def user_story_01(indDict, famDict):
  current_datetime = datetime.date(datetime.now())

  error_list = []

  for indId in indDict.keys():
    indInfo = indDict[indId]

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

  for famId in famDict.keys():
    famInfo = famDict[famId]

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
  current_datetime = datetime.date(datetime.now())

  error_list = []

  for famId in famDict.keys():
    famInfo = famDict[famId]

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

def user_story_07(indDict, famDict):
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

    if (deat[0] != "N/A"):
      deat_object = datetime.strptime(deat[0], '%d %b %Y').date()
      birt_object = datetime.strptime(birt[0], '%d %b %Y').date()
      age = deat_object.year - birt_object.year - \
        ((deat_object.month, deat_object.day) < (birt_object.month, birt_object.day))

      if (age > 150):
        error_list.append((deat[1], f'Error US07: Age of {name} is greater than 150.'))

    if (deat[0] == "N/A"):
      birt_object = datetime.strptime(birt[0], '%d %b %Y').date()
      age = current_datetime.year - birt_object.year - \
        ((current_datetime.month, current_datetime.day) < (birt_object.month, birt_object.day))

      if (age > 150):
        error_list.append((birt[1], f'Error US07: Age of {name} is greater than 150.'))
  return error_list

def user_story_08(indDict, famDict):
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
    div = famInfo['div']

    husb = indDict[husbId]['name'][0]
    wife = indDict[wifeId]['name'][0]

    chilInfo = famInfo['chil']

    for chil in chilInfo:
      chilId = chil[0]
      name = indDict[chilId]['name'][0]
      birt = indDict[chilId]['birt']

      if (marr[0] != "N/A"):
        birt_object = datetime.strptime(birt[0], '%d %b %Y').date()
        marr_object = datetime.strptime(marr[0], '%d %b %Y').date()

        if (birt_object < marr_object):
          error_list.append((birt[1], f'Error US08: Birth date of {name} is before the marriage date with {husb} and {wife}.'))
        
      if (div[0] != "N/A"):
        birt_object = datetime.strptime(birt[0], '%d %b %Y').date()
        div_object = (datetime.strptime(div[0], '%d %b %Y').date()) + relativedelta(months = 9)

        if (birt_object > div_object):
          error_list.append((birt[1], f'Error US08: Birth date of {name} is after the divorce date with {husb} and {wife}.'))

  return error_list

def user_story_10(indDict, famDict):
  error_list = []

  for famId in famDict.keys():
    famInfo = famDict[famId]

    id = famId
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]
    marr_date = famInfo['marr']
    div = famInfo['div']

    husbInfo = indDict[husbId]
    wifeInfo = indDict[wifeId]

    husb = husbInfo['name'][0]
    wife = wifeInfo['name'][0]

    husb_bd = wifeInfo['birt']
    wife_bd = wifeInfo['birt']

    if (marr_date[0] != 'N/A'):
      marr_date_obj = datetime.strptime(marr_date[0], '%d %b %Y').date()

      if (husb_bd[0] != 'N/A'):
        husb_bd_obj = datetime.strptime(husb_bd[0], '%d %b %Y').date()

        age_at_marriage = get_age_at_time(husb_bd_obj, marr_date_obj)

        if (age_at_marriage < 14):
          error_list.append((marr_date[1], f'Error US10: {husb} was younger than 14 when he got married to {wife}.'))

      if (wife_bd[0] != 'N/A'):
        wife_bd_obj = datetime.strptime(wife_bd[0], '%d %b %Y').date()

        age_at_marriage = get_age_at_time(wife_bd_obj, marr_date_obj)

        if (age_at_marriage < 14):
          error_list.append((marr_date[1], f'Error US10: {wife} was younger than 14 when she got married to {husb}.'))

  return error_list

def get_siblings(indDict, famDict):
  sibling_pairs = []

  for indId in indDict.keys():
    chil = get_children(famDict, indId)

    for i in range(len(chil)):
      for j in range(i+1, len(chil)):
        sibling_pairs.append((chil[i], chil[j]))
  
  return list(set([tuple(sorted(i)) for i in sibling_pairs]))

def get_children(famDict, indId):
  all_children = []
  for famId in famDict.keys():
    famInfo = famDict[famId]

    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]
    chil = famInfo['chil']

    if (husbId == indId or wifeId == indId):
      for child in chil:
        all_children.append(child[0])
  return all_children

def get_first_cousins(indDict, famDict):
  birth_siblings = get_siblings(indDict, famDict)
  first_cousins = []

  for sibling_pair in birth_siblings:
    a, b = sibling_pair
    a_chil = get_children(famDict, a)
    b_chil = get_children(famDict, b)

    for a_child in a_chil:
      for b_child in b_chil:
        first_cousins.append((a_child, b_child))
  return first_cousins

def user_story_18(indDict, famDict):
  siblings = get_siblings(indDict, famDict)

  error_list = []

  for famId in famDict.keys():
    famInfo = famDict[famId]

    line = famInfo['id'][1]
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]

    husb = indDict[husbId]['name'][0]
    wife = indDict[wifeId]['name'][0]

    for sibling_pair in siblings:
      if (sorted(sibling_pair) == sorted((husbId, wifeId))):
        error_list.append((line, f'Error US18: Siblings {husb} and {wife} should not be married.'))
  return error_list

def user_story_19(indDict, famDict):
  cousins = get_first_cousins(indDict, famDict)

  error_list = []

  for famId in famDict.keys():
    famInfo = famDict[famId]

    line = famInfo['id'][1]
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]

    husb = indDict[husbId]['name'][0]
    wife = indDict[wifeId]['name'][0]

    for cousin_pair in cousins:
      if (sorted(cousin_pair) == sorted((husbId, wifeId))):
        error_list.append((line, f'Error US19: Cousins {husb} and {wife} should not be married.'))
  return error_list

def print_errors(error_list, out):
  for error in error_list:
    # USER STORY 40:
    line_num = error[0]
    
    print(f'Line {line_num}: {error[1]}')
    out.write(f'Line {line_num}: {error[1]}\n')

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("requires an argument (filename)")

  indDict, famDict = analyse_gedcom(sys.argv[1])
  indDict, famDict = get_sorted_dicts(indDict, famDict)
  
  user_story_01_errors = user_story_01(indDict, famDict)

  user_story_02_errors = user_story_02(indDict, famDict)

  user_story_03_errors = birth_before_death(indDict)

  user_story_04_errors = marriage_before_divorce(famDict)

  user_story_05_errors = user_story_05(indDict, famDict)

  user_story_06_errors = user_story_06(indDict, famDict)

  user_story_18_errors = user_story_18(indDict, famDict)

  user_story_19_errors = user_story_19(indDict, famDict)

  with open('output.txt', 'w') as out:
    print_ged_tables(indDict, famDict, out)
    print('Errors')
    out.write('\nErrors\n')
    print_errors(user_story_01_errors, out)
    print_errors(user_story_02_errors, out)
    print_errors(user_story_03_errors, out)
    print_errors(user_story_04_errors, out)
    print_errors(user_story_05_errors, out)
    print_errors(user_story_06_errors, out)
    print_errors(user_story_18_errors, out)
    print_errors(user_story_19_errors, out)