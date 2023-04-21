# Elijah Wendel
# Kshitij Gugale
# I pledge my honor that I have abided by the Stevens Honor System.

import sys
import re
import time
import math
from prettytable import PrettyTable
from datetime import datetime
from dateutil.relativedelta import relativedelta

def list_recent_deaths(indDict, curr_date):
    """
    Lists the individuals who died in the last 30 days.
    """
    recent_deaths = []

    for indId in indDict.keys():
      indInfo = indDict[indId]

      deat = indInfo['deat'][0]
      name = indInfo['name'][0]

      if (deat != "N/A"):
        deat_object = datetime.strptime(deat, '%d %b %Y').date()
        if (within_last_30_days(deat_object, curr_date)):
          recent_deaths.append(f'{name}, {deat}')

    return recent_deaths

def list_recent_survivors(indDict, famDict, curr_date):
  recent_survivors = []

  for famId in famDict.keys():
    famInfo = famDict[famId]
    
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]

    husbName = indDict[husbId]['name'][0]
    wifeName = indDict[wifeId]['name'][0]

    husbDeat = indDict[husbId]['deat'][0]
    wifeDeat = indDict[wifeId]['deat'][0]

    marr = famInfo['marr'][0]
    div = famInfo['div'][0]
    chil = famInfo['chil']

    if (husbDeat != "N/A"):
      deat_object = datetime.strptime(husbDeat, '%d %b %Y').date()
      if (within_last_30_days(deat_object, curr_date)):
        if (wifeDeat == "N/A" and div == "N/A"):
          recent_survivors.append(wifeId)

        for child in chil:
          chilInfo = indDict[child[0]]
          chilDeat = chilInfo['deat'][0]

          if (chilDeat == "N/A"):
            recent_survivors.append(child[0])
    elif (wifeDeat != "N/A"):
      deat_object = datetime.strptime(wifeDeat, '%d %b %Y').date()
      if (within_last_30_days(deat_object, curr_date)):
        if (husbDeat == "N/A" and div == "N/A"):
          recent_survivors.append(husbId)

        for child in chil:
          chilInfo = indDict[child[0]]
          chilDeat = chilInfo['deat'][0]

          if (chilDeat == "N/A"):
            recent_survivors.append(child[0])

  recent_survivors = list(set(recent_survivors))

  recent_survivor_names = []

  for surv in recent_survivors:
    survInfo = indDict[surv]
    survName = survInfo['name'][0]
    recent_survivor_names.append(survName)

  return recent_survivor_names


def birth_before_death_of_parents(families, individuals):
    errors = []
    for fam_id, family in families.items():
        husband_id = family['husbId'][0]
        wife_id = family['wifeId'][0]
        children = family['chil']
        
        husb_line = family['husbId'][1]
        wife_line = family['wifeId'][1]

        husband = "N/A"
        wife = "N/A"

        # Skip validation if husband or wife is not listed in family record
        if not isinstance(husband_id, int) or not isinstance(wife_id, int):
            continue

        if husband_id not in individuals:
            errors.append((husb_line, f"ERROR: Family {fam_id}: Husband {husband_id} does not exist"))
        else:
            husband = individuals[husband_id]
            if husband['sex'][0] != 'M':
                errors.append((husb_line, f"ERROR: Family {fam_id}: Husband {husband_id} is not male"))

        if wife_id not in individuals:
            errors.append((wife_line, f"ERROR: Family {fam_id}: Wife {wife_id} does not exist"))
        else:
            wife = individuals[wife_id]
            if wife['sex'][0] != 'F':
                errors.append((wife_line, f"ERROR: Family {fam_id}: Wife {wife_id} is not female"))

        for chil in children:
            child_id = chil[0]
            chil_line = chil[1]
            if child_id not in individuals:
                errors.append((chil_line, f"ERROR: Family {fam_id}: Child {child_id} does not exist"))
            else:
                child = individuals[child_id]
                child_birth_date = datetime.strptime(child['birt'][0], '%d %b %Y').date()
                child_birth_line = child['birt'][1]
                
                if (husband != "N/A"):
                  husb_deat = husband['deat'][0]
                  if (husb_deat != "N/A"):
                    husb_deat_date_plus_nine_months = (datetime.strptime(husb_deat, '%d %b %Y') + relativedelta(months = 9)).date()
                    if (child_birth_date > husb_deat_date_plus_nine_months):
                      errors.append((child_birth_line, f"ERROR US09: Family {fam_id}: Child {child_id} born after 9 months after the death date of father."))
                
                if (wife != "N/A"):
                  wife_deat = wife['deat'][0]
                  if (wife_deat != "N/A"):
                    wife_deat_date = datetime.strptime(husb_deat, '%d %b %Y').date()
                    if (child_birth_date > wife_deat_date):
                      errors.append((child_birth_line, f"ERROR US09: Family {fam_id}: Child {child_id} born after 9 months after the death date of mother."))

    return errors

def output_results(individuals, families, errors):
    # ... existing code to output individuals and families ...

    if errors:
        print("\nErrors:")
        for error in errors:
            print(error)


def list_deceased(individuals):
    deceased = []
    for indi_id, indi in individuals.items():
        if indi.get('deat')[0] != "N/A":
            deceased.append(indi_id)
    return deceased

    
def output_results(individuals, families, errors, out, deceased=None):
    # ... existing code to output individuals and families ...

    if deceased:
        print("\nDeceased:")
        out.write("\nDeceased:")
        for indi_id in deceased:
            indi = individuals[indi_id]
            name = f"{indi.get('name', 'unknown name')[0]} ({indi_id})"
            death_date = indi.get('deat', '')
            print(f"{name}, died on {death_date[0]}")
            out.write(f"\n{name}, died on {death_date[0]}")


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

def get_age_at_time_in_dec(birth_date, time_to_compare):
  return (time_to_compare - birth_date).total_seconds() / 31556926

def next_anni_after(anni_date, curr_date):
  while (anni_date < curr_date):
    anni_date += relativedelta(years=1)
  return anni_date

def within_last_30_days(date, current_datetime):
  days = (current_datetime - date).total_seconds() / 86400
  return days <= 30 and days >= 0

def within_30_days(date, current_datetime):
  days = (next_anni_after(date, current_datetime) - current_datetime).total_seconds() / 86400
  return days <= 30 and days >= 0

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

def list_living_married(indDict, famDict):
    living_married = []
    for fam_id, family in famDict.items():
      husbId = family['husbId'][0]
      wifeId = family['wifeId'][0]
      marr = family['marr'][0]
      div = family['div'][0]

      if (marr != "N/A" and div == "N/A"):
        husbDeat = indDict[husbId]['deat'][0]
        wifeDeat = indDict[wifeId]['deat'][0]

        if (husbDeat == "N/A" and wifeDeat == "N/A"):
          living_married.append(indDict[husbId]['name'][0])
          living_married.append(indDict[wifeId]['name'][0])

    return living_married

def list_living_married_ids(indDict, famDict):
    living_married = []
    for fam_id, family in famDict.items():
      husbId = family['husbId'][0]
      wifeId = family['wifeId'][0]
      marr = family['marr'][0]
      div = family['div'][0]

      if (marr != "N/A" and div == "N/A"):
        husbDeat = indDict[husbId]['deat'][0]
        wifeDeat = indDict[wifeId]['deat'][0]

        if (husbDeat == "N/A" and wifeDeat == "N/A"):
          living_married.append(husbId)
          living_married.append(wifeId)

    return living_married

def list_living_single(indDict, famDict):
    living_single = []
    
    living_married_ids = list_living_married_ids(indDict, famDict)
    
    current_datetime = datetime.date(datetime.now())

    for indId in indDict.keys():
      if (indId in living_married_ids):
        continue

      indInfo = indDict[indId]

      id = indId
      name = indInfo['name'][0]
      birt = indInfo['birt'][0]
      deat = indInfo['deat'][0]

      

      birt_date = datetime.strptime(birt, '%d %b %Y').date()
      age = get_age_at_time(birt_date, current_datetime)
      
      if (age > 30 and deat == "N/A"):
        living_single.append(name)

    return living_single

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
    current_datetime = datetime.date(datetime.now())

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
          # USER STORY 27
          age = "N/A"

          sexEntry = ("N/A", 0)
          birtEntry = ("N/A", 0)
          deatEntry = ("N/A", 0)
          ageEntry = (age, 0)

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

                # USER STORY 28
                
          if (birt != "N/A"):
            birt_object = datetime.strptime(birt, '%d %b %Y').date()
            age = 0
            if (deat == "N/A"):
              age = get_age_at_time_in_dec(birt_object, current_datetime)
            else:
              deat_object = datetime.strptime(deat, '%d %b %Y').date()
              age = get_age_at_time_in_dec(birt_object, deat_object)
            ageEntry = (age, birtEntry[1])

          entry = {'id': idEntry, 'name': nameEntry, 'sex': sexEntry, 'deat': deatEntry, 'birt': birtEntry, 'age': ageEntry}
              
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

          idEntry = (int(num[0]), idx+1)
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
  indTable.field_names = ["Individual Id", "Name", "Sex", "Birthday", "Death Date", "Age"]

  famTable = PrettyTable()
  famTable.field_names = ["Family Id", "Husband", "Wife", "Marriage Date", "Divorce Date", "Children"]

  for ind in sortedIndDict.keys():
    indInfo = sortedIndDict[ind]

    id = ind
    name = indInfo['name'][0]
    sex = indInfo['sex'][0]
    birt = indInfo['birt'][0]
    deat = indInfo['deat'][0]
    age = math.floor(indInfo['age'][0])

    indTable.add_row([id, name, sex, birt, deat, age])

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
      chil.append(indDict[childId]['id'][0])
    
    sorted_siblings = user_story_28(indDict, chil)

    famTable.add_row([id, husb, wife, marr, div, sorted_siblings])

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

def user_story_28(indDict, siblings):

  siblings_with_age = []

  for sibling in siblings:
    siblingEntry = indDict[sibling]
    name = siblingEntry['name'][0]
    age = siblingEntry['age'][0]

    siblings_with_age.append((name, age))

  siblings_with_age.sort(key=lambda x: -x[1])
  siblings_names_only = []

  for sibling in siblings_with_age:
    siblings_names_only.append(sibling[0])

  return siblings_names_only

def user_story_32(indDict, famDict):
    indIds = list(indDict.keys())
    indIds.sort()

    familyIds = list(famDict.keys())
    familyIds.sort()
    sortedFamDict = {i: famDict[i] for i in familyIds}

    multiple_births_list = []

    for famId in sortedFamDict.keys():
      famInfo = sortedFamDict[famId]

      wifeId = famInfo['wifeId'][0]

      wife = indDict[wifeId]['name'][0]

      chilInfo = famInfo['chil']

      if (len(chilInfo) > 1):
        multiple_births_list.append(wife)
      
    return multiple_births_list

def user_story_33(indDict, famDict):
  indIds = list(indDict.keys())
  indIds.sort()

  familyIds = list(famDict.keys())
  familyIds.sort()
  sortedFamDict = {i: famDict[i] for i in familyIds}

  current_datetime = datetime.date(datetime.now())

  orphan_list = []

  for famId in sortedFamDict.keys():
    famInfo = sortedFamDict[famId]

    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]

    husb_deat = indDict[husbId]['deat'][0]
    wife_deat = indDict[wifeId]['deat'][0]

    chilInfo = famInfo['chil']

    if (husb_deat != "N/A" and wife_deat != "N/A"):

      for chil in chilInfo:
        chilId = chil[0]
        child = indDict[chilId]['name'][0]
        birt = indDict[chilId]['birt']
        birt_object = datetime.strptime(birt[0], '%d %b %Y').date()
        age = get_age_at_time(birt_object, current_datetime)

        if (age < 18):
          orphan_list.append(child)

  return orphan_list

def user_story_34(indDict, famDict):
    indIds = list(indDict.keys())
    indIds.sort()

    familyIds = list(famDict.keys())
    familyIds.sort()
    sortedFamDict = {i: famDict[i] for i in familyIds}

    large_age_diff_list = []

    for famId in sortedFamDict.keys():
      famInfo = sortedFamDict[famId]

      husbId = famInfo['husbId'][0]
      wifeId = famInfo['wifeId'][0]

      husband = indDict[husbId]['name'][0]
      wife = indDict[wifeId]['name'][0]

      marr = famInfo['marr'][0]

      if (marr != "N/A"):
        marr_object = datetime.strptime(marr, '%d %b %Y').date()

        husb_birt = indDict[husbId]['birt']
        husb_birt_object = datetime.strptime(husb_birt[0], '%d %b %Y').date()
        husb_age = get_age_at_time(husb_birt_object, marr_object)

        wife_birt = indDict[wifeId]['birt']
        wife_birt_object = datetime.strptime(wife_birt[0], '%d %b %Y').date()
        wife_age = get_age_at_time(wife_birt_object, marr_object)

        if (husb_age > 2 * wife_age or wife_age > 2 * husb_age):
          large_age_diff_list.append((husband, wife))
          
    return large_age_diff_list

def user_story_35(indDict, famDict, curr_date):
  recent_births_list = []
  
  for indId in indDict.keys():
    indInfo = indDict[indId]

    birt = indInfo['birt'][0]
    name = indInfo['name'][0]


    if (birt != 'N/A'):
      birt_object = datetime.strptime(birt, '%d %b %Y').date()
      if (within_last_30_days(birt_object, curr_date)):
        recent_births_list.append(name)

  return recent_births_list

def user_story_38(indDict, curr_date):
  
  upcoming_bdays = []

  for indId in indDict.keys():
    indInfo = indDict[indId]

    birt = indInfo['birt'][0]
    deat = indInfo['deat'][0]
    name = indInfo['name'][0]

    if (birt != 'N/A' and deat == "N/A"):
      birt_object = datetime.strptime(birt, '%d %b %Y').date()
      if (within_30_days(birt_object, curr_date)):
        upcoming_bdays.append(f'{name}, {birt}')

  return upcoming_bdays

def user_story_39(indDict, famDict, curr_date):
  
  upcoming_annis = []

  for famId in famDict.keys():
    famInfo = famDict[famId]
    
    husbId = famInfo['husbId'][0]
    wifeId = famInfo['wifeId'][0]

    husbName = indDict[husbId]['name'][0]
    wifeName = indDict[wifeId]['name'][0]

    husbDeat = indDict[husbId]['deat'][0]
    wifeDeat = indDict[wifeId]['deat'][0]

    marr = famInfo['marr'][0]
    div = famInfo['div'][0]

    if (marr != 'N/A' and div == "N/A" and husbDeat == "N/A" and wifeDeat == "N/A"):
      marr_object = datetime.strptime(marr, '%d %b %Y').date()
      if (within_30_days(marr_object, curr_date)):
        upcoming_annis.append(f'{husbName} & {wifeName}, {marr}')

  return upcoming_annis

def print_errors(error_list, out):
  for error in error_list:
    # USER STORY 40:
    line_num = error[0]
    
    print(f'Line {line_num}: {error[1]}')
    out.write(f'Line {line_num}: {error[1]}\n')

def print_list(header, data_list, out):
  print(header)
  out.write(header + '\n')

  if len(data_list) == 0:
    print('None')
    out.write(f'None\n')

  for data in data_list:
    
    print(f'{data}')
    out.write(f'{data}\n')

if __name__ == "__main__":

  if len(sys.argv) < 2:
    print("requires an argument (filename)")
  individuals, families = analyse_gedcom(sys.argv[1])
  errors = []
  #errors += validate_individuals(individuals)
  errors += birth_before_death_of_parents(families, individuals)

    # Call the new function to get the list of deceased individuals
  deceased = list_deceased(individuals)
  
  indDict, famDict = analyse_gedcom(sys.argv[1])
  indDict, famDict = get_sorted_dicts(indDict, famDict)
  
  user_story_01_errors = user_story_01(indDict, famDict)

  user_story_02_errors = user_story_02(indDict, famDict)

  user_story_03_errors = birth_before_death(indDict)

  user_story_04_errors = marriage_before_divorce(famDict)

  user_story_05_errors = user_story_05(indDict, famDict)

  user_story_06_errors = user_story_06(indDict, famDict)

  user_story_07_errors = user_story_07(indDict, famDict)

  user_story_08_errors = user_story_08(indDict, famDict)

  user_story_09_errors = birth_before_death_of_parents(famDict, indDict)

  user_story_10_errors = user_story_10(indDict, famDict)

  user_story_18_errors = user_story_18(indDict, famDict)

  user_story_19_errors = user_story_19(indDict, famDict)

  user_story_30_list = list_living_married(indDict, famDict)

  user_story_31_list = list_living_single(indDict, famDict)

  user_story_32_list = user_story_32(indDict, famDict)
  
  user_story_33_list = user_story_33(indDict, famDict)

  user_story_34_list = user_story_34(indDict, famDict)

  user_story_35_list = user_story_35(indDict, famDict, datetime.now().date())

  user_story_36_list = list_recent_deaths(indDict, datetime.now().date())

  user_story_37_list = list_recent_survivors(indDict, famDict, datetime.now().date())

  user_story_38_list = user_story_38(indDict, datetime.now().date())

  user_story_39_list = user_story_39(indDict, famDict, datetime.now().date())

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
    print_errors(user_story_07_errors, out)
    print_errors(user_story_08_errors, out)
    print_errors(user_story_09_errors, out)
    print_errors(user_story_10_errors, out)
    print_errors(user_story_18_errors, out)
    print_errors(user_story_19_errors, out)
    output_results(indDict, famDict, errors, out, deceased)
    out.write("\n\n")
    print_list("Living Married (US30):", user_story_30_list, out)
    out.write("\n")
    print_list("Living Single (US31):",user_story_31_list, out)
    out.write("\n")
    print_list("Multiple Births (US32):",user_story_32_list, out)
    out.write("\n")
    print_list("Orphans (US33):",user_story_33_list, out)
    out.write("\n")
    print_list("Couples with large age differences (US34):",user_story_34_list, out)
    out.write("\n")
    print_list("Births within last 30 days (US35):",user_story_35_list, out)
    out.write("\n")
    print_list("Deaths within last 30 days (US36):",user_story_36_list, out)
    out.write("\n")
    print_list("Survivors within last 30 days (US37):",user_story_37_list, out)
    out.write("\n")
    print_list("Birthdays within 30 days (US38):",user_story_38_list, out)
    out.write("\n")
    print_list("Anniversaries within 30 days (US39):",user_story_39_list, out)
    out.write("\n")


