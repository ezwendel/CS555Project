import unittest

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
    actual_errors = p2.use_case_01(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

  def test_futurechild_US01(self):
    expected_errors = [
      (38,'Error US01: Birth date of FutureChild Normal is after the current date.')
    ]

    indDict, famDict = p2.analyse_gedcom('.\\TestGedcomFiles\\US01_futurechild.ged')
    actual_errors = p2.use_case_01(indDict, famDict)

    self.assertListEqual(expected_errors, actual_errors)

if __name__ == '__main__':
    unittest.main()