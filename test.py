import sys
import re
import prettytable
from datetime import datetime

def birth_before_death(indDict):
    for id, entry in indDict.items():
        birt_date = entry['birt'][0]
        deat_date = entry['deat'][0]
        
        if birt_date != "N/A" and deat_date != "N/A":
            birt = datetime.strptime(birt_date, '%d %b %Y')
            deat = datetime.strptime(deat_date, '%d %b %Y')
            
            if birt > deat:
                print(f"ERROR: Individual {id} has birth date ({birt_date}) after death date ({deat_date}).")

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
                                newLine = lines[i
