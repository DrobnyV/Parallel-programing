import unittest

from menu import Menu


class UnitTests(unittest.TestCase):
    def test_input_check(self):
        with self.assertRaises(TypeError):
            Menu.check_if_int("a")




if __name__ == '__main__':
    unittest.main()