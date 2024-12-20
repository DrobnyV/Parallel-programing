import threading
import unittest
from unittest.mock import patch, MagicMock

from UI.interactive_menu import InteractiveMenu
from examples.message import Messages
from examples.shared_memory import SharedMemory

from config.config import Config


class TestMessages(unittest.TestCase):
    def setUp(self):
        self.messages = Messages()
        self.messages.config = Config()
        self.messages.config.data = {"message_count": 3, "delay_between_messages": 1}

    def test_producer(self):
        self.messages.producer()
        self.assertEqual(self.messages.message_queue.qsize(), 3)

    def test_consumer(self):
        for i in range(3):
            self.messages.message_queue.put(f"Message {i}")
        self.messages.consumer()
        self.assertTrue(self.messages.message_queue.empty())


class TestSharedMemory(unittest.TestCase):
    def setUp(self):
        self.shared_memory = SharedMemory()
        self.shared_memory.config = Config()
        self.shared_memory.config.data = {"max_threads": 2, "delay_between_messages": 0}

    def test_counter_increment(self):
        threads = [
            threading.Thread(target=self.shared_memory.increment, args=(f"Thread-{i}",))
            for i in range(2)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(self.shared_memory.counter, 200000)

class TestInteractiveMenu(unittest.TestCase):
    def setUp(self):
        self.menu = InteractiveMenu()
        self.menu.config.data = {
            "message_count": 5,
            "delay_between_messages": 2,
            "max_threads": 10,
            "use_colors": True
        }

    def test_config_add_new_key(self):
        # Add a new configuration key
        self.menu.do_config('new_key 123')
        self.assertEqual(self.menu.config.get('new_key'), '123')

    def test_config_update_existing_key(self):
        # Update an existing configuration key
        self.menu.do_config('message_count 10')
        self.assertEqual(self.menu.config.get('message_count'), 10)

    def test_config_invalid_input(self):
        # Test invalid input format
        with patch('builtins.print') as mock_print:
            self.menu.do_config('invalid input extra')
            mock_print.assert_called_with("Usage: config [key] [value] or config to view all configs")

    def test_config_boolean_values(self):
        # Test setting boolean values
        self.menu.do_config('use_colors false')
        self.assertFalse(self.menu.config.get('use_colors'))

        self.menu.do_config('use_colors true')
        self.assertTrue(self.menu.config.get('use_colors'))

    def test_config_numeric_values(self):
        self.menu.do_config('delay_between_messages 5')
        self.assertEqual(self.menu.config.get('delay_between_messages'), 5)  # Expect integer

        self.menu.config.set('delay_between_messages', 0.5)  # Explicitly set float value
        self.assertEqual(self.menu.config.get('delay_between_messages'), 0.5)

    def test_run_messages_simulation(self):
        with patch.object(Messages, 'run', return_value=None) as mock_run:
            self.menu.do_messages('run')
            mock_run.assert_called_once()

    def test_show_messages_simulation_code(self):
        with patch.object(Messages, 'show_code', return_value=None) as mock_show_code:
            self.menu.do_messages('show')
            mock_show_code.assert_called_once()

    def test_run_shared_memory_simulation(self):
        with patch.object(SharedMemory, 'run', return_value=None) as mock_run:
            self.menu.do_shared_memory('run')
            mock_run.assert_called_once()

    def test_show_shared_memory_simulation_code(self):
        with patch.object(SharedMemory, 'show_code', return_value=None) as mock_show_code:
            self.menu.do_shared_memory('show')
            mock_show_code.assert_called_once()

    def test_invalid_command(self):
        with patch('builtins.print') as mock_print:
            self.menu._handle_command('nonexistent_simulation', 'run')
            mock_print.assert_called_with(f"\033[91mSimulation 'nonexistent_simulation' not found.\033[0m")

    def test_config_view_all(self):
        with patch('builtins.print') as mock_print:
            self.menu._show_all_config()
            mock_print.assert_any_call("message_count: 5")
            mock_print.assert_any_call("delay_between_messages: 2")
            mock_print.assert_any_call("max_threads: 10")
            mock_print.assert_any_call("use_colors: True")

    def test_config_missing_key(self):
        with patch('builtins.print') as mock_print:
            self.menu._show_config('nonexistent_key')
            mock_print.assert_called_with("Configuration key 'nonexistent_key' not found.")

    def test_config_update_file(self):
        with patch('json.dump') as mock_json_dump, patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            self.menu.do_config('test_key 99')

            # Check that the file is opened correctly
            mock_file.assert_called_with('config.json', 'w')

            # Check that json.dump is called with the expected data
            mock_json_dump.assert_called_once_with(self.menu.config.data, mock_file(), indent=4)

    def test_config_propagation_to_simulations(self):
        # Update the configuration
        self.menu.do_config('message_count 10')
        self.menu.do_config('delay_between_messages 1')

        # Check if the configuration propagated to Messages
        messages_sim = self.menu.simulations['messages']
        self.assertEqual(messages_sim.config.get('message_count'), 10)
        self.assertEqual(messages_sim.config.get('delay_between_messages'), 1)

        # Check if the configuration propagated to SharedMemory
        shared_memory_sim = self.menu.simulations['shared_memory']
        self.assertEqual(shared_memory_sim.config.get('message_count'), 10)  # Shared config
        self.assertEqual(shared_memory_sim.config.get('delay_between_messages'), 1)





if __name__ == "__main__":
    unittest.main()
