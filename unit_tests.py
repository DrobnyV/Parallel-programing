import unittest
from unittest.mock import patch
from io import StringIO

from UI.interactive_menu import InteractiveMenu
from color import Color
from examples.message import Messages
from examples.shared_memory import SharedMemory


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.menu = InteractiveMenu()
        self.messages_sim = Messages()
        self.shared_mem_sim = SharedMemory()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input',
           side_effect=['messages run', 'messages show', 'shared_memory run', 'shared_memory show', 'EOF'])
    def test_menu_commands(self, mock_input, mock_stdout):
        self.menu.cmdloop()
        output = mock_stdout.getvalue()

        # Check for specific outputs from simulations
        self.assertIn("Producer: Sent message", output)  # Check if messages simulation ran
        self.assertIn("def producer(self):", output)  # Check if messages simulation code was shown
        self.assertIn("Thread-1: Counter is now", output)  # Check if shared memory simulation ran
        self.assertIn("def increment(self, thread_name):", output)  # Check if shared memory code was shown

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['messages wrong', 'EOF'])
    def test_invalid_command(self, mock_input, mock_stdout):
        self.menu.cmdloop()
        output = mock_stdout.getvalue()
        self.assertIn("Invalid command. Use 'run' or 'show'.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['exit'])
    def test_exit_command(self, mock_input, mock_stdout):
        self.menu.cmdloop()
        output = mock_stdout.getvalue()
        self.assertIn("Exiting...", output)

    def test_messages_simulation(self):
        # Checks if the methods exist for the messages simulation
        self.assertTrue(hasattr(self.messages_sim, 'producer'))
        self.assertTrue(hasattr(self.messages_sim, 'consumer'))
        self.messages_sim.run()  # This won't verify threading but ensures it runs without exceptions

    def test_shared_memory_simulation(self):
        # Here we test if the simulation runs to completion
        self.shared_mem_sim.run()
        # Since we can't directly test threading, we'll check if the counter ends up at least at some value
        self.assertGreaterEqual(self.shared_mem_sim.counter, 100000)  # Assuming counter starts at 0 and increments

    @patch('sys.stdout', new_callable=StringIO)
    def test_color_codes(self, mock_stdout):
        # Test if color codes are correctly defined
        self.assertEqual(Color.RED, '\033[91m')
        self.assertEqual(Color.GREEN, '\033[92m')
        self.assertEqual(Color.BLUE, '\033[94m')


if __name__ == '__main__':
    unittest.main()