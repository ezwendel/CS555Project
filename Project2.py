# Elijah Wendel
# I pledge my honor that I have abided by the Stevens Honor System.

import re

out = open("output.txt", "w")

def printer(line, valid):
  line = line.strip()
  out.write("--> " + line)
  out.write("\n")
  parts = line.split(" ")
  yn = ""
  if (valid):
    yn = "Y"
  else:
    yn = "N"

  if (len(parts) < 2):
    out.write("<-- " + line + "|" + yn)
  elif (len(parts) == 2):
    level = parts[0]
    tag = parts[1]
    out.write("<-- " + level + "|" + "|".join([tag, yn]) + "|")
  else:
    level = parts[0]
    tag = parts[1]
    arg = " ".join(parts[2:])
    out.write("<-- " + level + "|" + "|".join([tag, yn, arg]))
  out.write("\n")
  

gedFile = open("gedcomfile.ged")
lines = gedFile.readlines()
tags0 = ["HEAD", "TRLR", "NOTE"]
tags1famId = ["FAMC", "FAMS"]
tags1indId = ["HUSB", "WIFE", "CHIL"]
tags1none = ["BIRT", "DEAT", "MARR", "DIV"]
tags2 = ["DATE"]
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

for line in lines:
  line = line.strip()
  parts = line.split(" ")
  if (len(parts) == 2):
    tag = parts[1]
    level = parts[0]
    if (level == "0" and tag in tags0):
      printer(line, True)
    elif (level == "1" and tag in tags1none):
      printer(line, True)
    else:
      printer(line, False)
  elif (len(parts) < 3):
    printer(line, False)
  else:
    if (parts[2] == "INDI"):
      iidValid = re.search("^@I\d+@$", parts[1])
      printer(line, bool(parts[0] == "0" and bool(iidValid)))
    elif (parts[2] == "FAM"):
      fidValid = re.search("^@F\d+@$", parts[1])
      printer(line, bool(parts[0] == "0" and bool(fidValid)))
    else:
      arg = " ".join(parts[2:])
      tag = parts[1]
      level = parts[0]
      if (level == "0" and tag in tags0):
        if (tag == "NOTE"):
          printer(line, True)
        else:
          printer(line, False)
      elif (level == "1" and tag == "SEX"):
        printer(line, arg == "F" or arg == "M")
      elif (level == "1" and tag == "NAME"):
        printer(line, arg != "")
      elif (level == "1" and tag in tags1indId):
        iidValid = re.search("^@I\d+@$", arg)
        printer(line, bool(iidValid))
      elif (level == "1" and tag in tags1famId):
        fidValid = re.search("^@F\d+@$", arg)
        printer(line, bool(fidValid))
      elif (level == "2" and tag == "DATE"):
        dateList = arg.split(" ")
        if (len(dateList) != 3):
          printer(line, False)
        else:
          if (bool(re.search("^\d+$", dateList[0])) and bool(re.search("^\d+$", dateList[2]))):
            dateNum = int(dateList[0])
            printer(line, dateNum > 0 and dateNum <= 31 and dateList[1] in months)
          else:
            printer(line, False)
      else:
        printer(line, False)
