import unittest

from menu import Menu


class UnitTests(unittest.TestCase):
    def test_input_check(self):
        self.assertFalse(Menu.is_convertible_to_int("a"))




if __name__ == '__main__':
    unittest.main()