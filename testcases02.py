import io
import sys
import unittest
from datetime import datetime

from gedcom_parser import analyse_gedcom

class TestBirthBeforeDeath(unittest.TestCase):
    def test_valid_birth_before_death(self):
        # Valid case where birth date is before death date
        gedcom = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 BIRT
        2 DATE 01 JAN 1900
        1 DEAT
        2 DATE 01 JAN 1980
        """
        expected_output = "All individuals have a valid birth date before their death date.\n"
        self.assertEqual(run_test_with_input(gedcom), expected_output)

    def test_invalid_birth_after_death(self):
        # Invalid case where birth date is after death date
        gedcom = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 BIRT
        2 DATE 01 JAN 1980
        1 DEAT
        2 DATE 01 JAN 1900
        """
        expected_output = "Error: Individual @I1@ has an invalid birth date after their death date.\n"
        self.assertEqual(run_test_with_input(gedcom), expected_output)

    def test_missing_birth_or_death_date(self):
        # Invalid case where birth date or death date is missing
        gedcom = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 BIRT
        2 DATE 01 JAN 1900
        """
        expected_output = "Error: Individual @I1@ is missing a death date.\n"
        self.assertEqual(run_test_with_input(gedcom), expected_output)

    def test_valid_birth_missing_death_date(self):
        # Valid case where death date is missing
        gedcom = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 BIRT
        2 DATE 01 JAN 1900
        """
        expected_output = "All individuals have a valid birth date before their death date.\n"
        self.assertEqual(run_test_with_input(gedcom), expected_output)

def run_test_with_input(gedcom):
    saved_stdout = sys.stdout
    try:
        out = io.StringIO()
        sys.stdout = out
        analyse_gedcom(io.StringIO(gedcom))
        output = out.getvalue()
    finally:
        sys.stdout = saved_stdout
    return output

if __name__ == '__main__':
    unittest.main()
