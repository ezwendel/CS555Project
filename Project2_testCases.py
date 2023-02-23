import unittest
import sys
import io

import Project2 as p2

class TestUseCases(unittest.TestCase):

  def test_farnsworth_US01(self):
    expected_errors = [
      (20, 'Error US01: Birth date of Hubert Farnsworth is after the current date.'),
      (29, 'Error US01: Birth date of Ned Farnsworth is after the current date.'),
      (31, 'Error US01: Death date of Ned Farnsworth is after the current date.'),
      (40, 'Error US01: Birth date of Velma Bolton is after the current date.'),
      (47, 'Error US01: Marriage date of Ned Farnsworth and Velma Bolton is after the current date.'),
      (49, 'Error US01: Divorce date of Ned Farnsworth and Velma Bolton is after the current date.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US01_farnsworth.ged')
    actual_errors = p2.user_story_01(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_futurechild_US01(self):
    expected_errors = [(38,'Error US01: Birth date of Child Future is after the current date.')]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US01_futurechild.ged')
    actual_errors = p2.user_story_01(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_normal_US01(self):
    expected_errors = []

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US01_normal.ged')
    actual_errors = p2.user_story_01(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_futuredeath_US01(self):
    expected_errors = [(22, 'Error US01: Death date of Guy WhoWillDie is after the current date.')]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US01_futuredeath.ged')
    actual_errors = p2.user_story_01(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)
  
  def test_futuremarriage_US01(self):
    expected_errors = [(45, 'Error US01: Marriage date of Incorrect Marriage and Weird Union is after the current date.')]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US01_futuremarriage.ged')
    actual_errors = p2.user_story_01(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_bothmarriedearly_US02(self):
    expected_errors = [
      (29, 'Error US02: Birth date of Too Early is after the marriage date with Married BeforeBorn.'),
      (20,'Error US02: Birth date of Married BeforeBorn is after the marriage date with Too Early.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US02_bothmarriedearly.ged')
    actual_errors = p2.user_story_02(indDict, famDict)

    self.assertCountEqual(expected_errors, actual_errors)

  def test_wifemarriedbeforebirth_US02(self):
    expected_errors = [
      (20,'Error US02: Birth date of Married BeforeBorn is after the marriage date with NotToo Early.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US02_wifemarriedbeforebirth.ged')
    actual_errors = p2.user_story_02(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_husbmarriedbeforebirth_US02(self):
    expected_errors = [
      (29, 'Error US02: Birth date of Too Early is after the marriage date with NotMarried BeforeBorn.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US02_husbmarriedbeforebirth.ged')
    actual_errors = p2.user_story_02(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_siblingmarriage_US18(self):
    expected_errors = [
      (44, 'Error US18: Siblings Bro Ther and Daugh Ther should not be married.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US18_siblingmarriage.ged')
    actual_errors = p2.user_story_18(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_cousinmarriage_US19(self):
    expected_errors = [
      (95, 'Error US19: Cousins Bro2 Ther and Daugh Ther should not be married.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US19_cousinmarriage.ged')
    actual_errors = p2.user_story_19(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_undead_US03(self):
    expected_errors = [
      (20, 'ERROR US03: Individual 1 has birth date (4 FEB 2020) after death date (2 MAR 2019).')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\undead.ged')
    actual_errors = p2.birth_before_death(indDict)

    self.assertListEqual(expected_errors, actual_errors)
  
  def test_undead_US04(self):
    expected_errors = [
      (35, 'ERROR US04: Family 1 has marriage date (7 MAR 2022) after divorce date (5 JUL 2021).')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\undead.ged')
    actual_errors = p2.marriage_before_divorce(famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_undead_US05(self):
    expected_errors = [
      (22, 'Error US05: Death date of Undead Guy is before the marriage date with Normal Person.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\undead.ged')
    actual_errors = p2.user_story_05(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)
  
  def test_undead_US06(self):
    expected_errors = [
      (22, 'Error US06: Death date of Undead Guy is before the divorce date with Normal Person.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\undead.ged')
    actual_errors = p2.user_story_06(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_US07(self):
    expected_errors = [(22,'Error US07: Age of Too Old is greater than 150.')]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US07_lessthan150.ged')
    actual_errors = p2.user_story_07(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_US08(self):
    expected_errors = [
      (20,'Error US08: Birth date of Birth BeforeMarriage is before the marriage date with Husband BeforeMarriage and Wife BeforeMarriage.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US08_birthbeforemarriage.ged')
    actual_errors = p2.user_story_08(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_US10(self):
    expected_errors = []

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\undead.ged')
    actual_errors = p2.user_story_10(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_US10(self):
    expected_errors = [
      (35, 'Error US10: Guy Young was younger than 14 when he got married to Girl Young.'),
      (35, 'Error US10: Girl Young was younger than 14 when she got married to Guy Young.')]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US10_youngmarriage.ged')
    actual_errors = p2.user_story_10(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)
  
  def test_undead_US40(self):
    expected_out = str('Line 22: Error US06: Death date of Undead Guy is before the divorce date with Normal Person.\n')

    out = io.StringIO("")

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\undead.ged')
    actual_errors = p2.user_story_06(indDict, famDict)

    p2.print_errors(actual_errors, out)

    actual_out = str(out.getvalue())

    print(expected_out)
    print(actual_out)

    self.assertEqual(expected_out, actual_out)

  def test_cousinmarriage_US40(self):
    expected_out = str('Line 95: Error US19: Cousins Bro2 Ther and Daugh Ther should not be married.\n')

    out = io.StringIO("")

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US19_cousinmarriage.ged')
    actual_errors = p2.user_story_19(indDict, famDict)

    p2.print_errors(actual_errors, out)

    actual_out = str(out.getvalue())

    print(expected_out)
    print(actual_out)

    self.assertEqual(expected_out, actual_out)

if __name__ == '__main__':
    unittest.main()