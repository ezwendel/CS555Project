import unittest

import Project2 as p2

class TestUseCases(unittest.TestCase):

  def test_list_living_married():
    expected_errors= []
    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US01_farnsworth.ged')
    actual_errors = p2.user_story_01(indDict, famDict)

  def test_list_living_single():
    expected_errors = []
    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US01_farnsworth.ged')
    actual_errors = p2.user_story_01(indDict, famDict)

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
  

if __name__ == '__main__':
    unittest.main()