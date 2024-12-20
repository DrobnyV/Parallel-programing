import unittest
from unittest.mock import patch
from io import StringIO

from color import Color
from menu import Menu
from examples.message import Messages
from examples.shared_memory import SharedMemory

class UnitTests(unittest.TestCase):
    def setUp(self):
        self.menu = Menu()
        self.messages_sim = Messages()
        self.shared_mem_sim = SharedMemory()

    @patch('sys.stdout', new_callable=StringIO)
    def test_menu_display(self, mock_stdout):
        self.menu.display()
        output = mock_stdout.getvalue()
        self.assertIn("Messages", output)
        self.assertIn("SharedMemory", output)  # Assuming this class name in the menu

    @patch('builtins.input', side_effect=['1', '1', 'q', '2', '2', 'q'])  # 'q' can be used to exit the loop
    @patch('sys.stdout', new_callable=StringIO)
    def test_menu_navigation(self, mock_stdout, mock_input):
        # Modify the Menu class to handle 'q' as an exit command
        # This is just an example, adjust according to your actual implementation
        self.menu.run()
        output = mock_stdout.getvalue()
        self.assertIn("Messages", output)  # Check if Messages simulation was accessed
        self.assertIn("Show code", output)  # Check if show code option was accessed
        self.assertIn("SharedMemory", output)  # Check if SharedMemory simulation was accessed

    def test_messages_simulation(self):
        # This test can't check the actual threading behavior but can check if methods exist
        self.assertTrue(hasattr(self.messages_sim, 'producer'))
        self.assertTrue(hasattr(self.messages_sim, 'consumer'))
        self.messages_sim.run()  # This won't verify threading but ensures it runs without exceptions

    def test_shared_memory_simulation(self):
        # Here we test if the simulation runs to completion
        self.shared_mem_sim.run()
        # Since we can't directly test threading, we'll check if the counter ends up at least at some value
        self.assertGreaterEqual(self.shared_mem_sim.counter, 100000)  # Assuming counter starts at 0 and increments

    def test_input_check(self):
        self.assertFalse(Menu.is_convertible_to_int("a"))
        self.assertTrue(Menu.is_convertible_to_int("1"))

    @patch('sys.stdout', new_callable=StringIO)
    def test_color_codes(self, mock_stdout):
        # Test if color codes are correctly defined
        self.assertEqual(Color.RED, '\033[91m')
        self.assertEqual(Color.GREEN, '\033[92m')
        self.assertEqual(Color.BLUE, '\033[94m')

if __name__ == '__main__':
    unittest.main()