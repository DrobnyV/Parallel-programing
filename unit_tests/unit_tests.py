import threading
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open

import numpy as np

from UI.interactive_menu import InteractiveMenu
from examples.message import Messages
from examples.mp_calculation import MultiprocessingSimulation
from examples.mp_word_count import WordCountSimulation
from examples.prime_number_cal import PrimeNumberSimulation, is_prime
from examples.shared_memory import SharedMemory

from config.config import Config
from examples.thread_synchronization import ThreadSynchronization


class TestMessages(unittest.TestCase):
    def setUp(self):
        self.messages = Messages()
        self.messages.config = Config()
        self.messages.config.data = {"message_count": 3, "delay_between_messages": 1}

    def test_producer(self):
        """
        Test if the producer correctly adds messages to the queue.
        """
        self.messages.producer()
        self.assertEqual(self.messages.message_queue.qsize(), 3)

    def test_consumer(self):
        """
        Test if the consumer correctly removes messages from the queue.
        """
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
        """
        Test if the shared counter increments correctly with multiple threads.
        """
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
        """
        Test adding a new configuration key.
        """
        self.menu.do_config('new_key 123')
        self.assertEqual(self.menu.config.get('new_key'), '123')

    def test_config_update_existing_key(self):
        """
        Test updating an existing configuration key.
        """
        self.menu.do_config('message_count 10')
        self.assertEqual(self.menu.config.get('message_count'), 10)

    def test_config_invalid_input(self):
        """
        Test handling of invalid configuration input format.
        """
        with patch('builtins.print') as mock_print:
            self.menu.do_config('invalid input extra')
            mock_print.assert_called_with("Usage: config [key] [value] or config to view all configs")

    def test_config_boolean_values(self):
        """
        Test setting boolean values in the configuration.
        """
        self.menu.do_config('use_colors false')
        self.assertFalse(self.menu.config.get('use_colors'))

        self.menu.do_config('use_colors true')
        self.assertTrue(self.menu.config.get('use_colors'))

    def test_config_numeric_values(self):
        """
        Test setting numeric values in the configuration.
        """
        self.menu.do_config('delay_between_messages 5')
        self.assertEqual(self.menu.config.get('delay_between_messages'), 5)  # Expect integer

        self.menu.config.set('delay_between_messages', 0.5)  # Explicitly set float value
        self.assertEqual(self.menu.config.get('delay_between_messages'), 0.5)

    def test_run_messages_simulation(self):
        """
        Test running the Messages simulation through the menu.
        """
        with patch.object(Messages, 'run', return_value=None) as mock_run:
            self.menu.do_messages('run')
            mock_run.assert_called_once()

    def test_show_messages_simulation_code(self):
        """
        Test showing the code for the Messages simulation.
        """
        with patch.object(Messages, 'show_code', return_value=None) as mock_show_code:
            self.menu.do_messages('show')
            mock_show_code.assert_called_once()

    def test_run_shared_memory_simulation(self):
        """
        Test running the Shared Memory simulation through the menu.
        """
        with patch.object(SharedMemory, 'run', return_value=None) as mock_run:
            self.menu.do_shared_memory('run')
            mock_run.assert_called_once()

    def test_show_shared_memory_simulation_code(self):
        """
        Test showing the code for the Shared Memory simulation.
        """
        with patch.object(SharedMemory, 'show_code', return_value=None) as mock_show_code:
            self.menu.do_shared_memory('show')
            mock_show_code.assert_called_once()

    def test_invalid_command(self):
        """
        Test handling an invalid simulation command.
        """
        with patch('builtins.print') as mock_print:
            self.menu._handle_command('nonexistent_simulation', 'run')
            mock_print.assert_called_with(f"\033[91mSimulation 'nonexistent_simulation' not found.\033[0m")

    def test_config_view_all(self):
        """
        Test displaying all configuration settings.
        """
        with patch('builtins.print') as mock_print:
            self.menu._show_all_config()
            mock_print.assert_any_call("message_count: 5")
            mock_print.assert_any_call("delay_between_messages: 2")
            mock_print.assert_any_call("max_threads: 10")
            mock_print.assert_any_call("use_colors: True")

    def test_config_missing_key(self):
        """
        Test displaying a message for a missing configuration key.
        """
        with patch('builtins.print') as mock_print:
            self.menu._show_config('nonexistent_key')
            mock_print.assert_called_with("Configuration key 'nonexistent_key' not found.")

    def test_config_update_file(self):
        """
        Test if updating configuration writes to the file correctly.
        """
        with patch('json.dump') as mock_json_dump, patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            self.menu.do_config('test_key 99')

            # Check that the file is opened correctly
            mock_file.assert_called_with('config.json', 'w')

            # Check that json.dump is called with the expected data
            mock_json_dump.assert_called_once_with(self.menu.config.data, mock_file(), indent=4)

    def test_config_propagation_to_simulations(self):
        """
        Test that configuration changes propagate to all simulations.
        """
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

class TestThreadSynchronization(unittest.TestCase):
    def setUp(self):
        self.simulation = ThreadSynchronization()
        self.simulation.config.data = {
            "num_threads": 3,
            "delay_between_stages": 0.1  # Shorten for testing
        }

    def test_barrier_synchronization(self):
        """
        Test if threads synchronize correctly at barriers.
        """
        with patch('builtins.print') as mock_print:
            self.simulation.run()
            # Check that the print statements indicate threads pass the barrier together
            mock_print.assert_any_call("\033[92mThread-0: Starting stage 1\033[0m")
            mock_print.assert_any_call("\033[94mThread-0: Waiting at barrier for stage 1\033[0m")
            mock_print.assert_any_call("\033[93mThread-0: Passed barrier for stage 1\033[0m")

    def test_thread_execution(self):
        """
        Test if all threads execute all stages of the simulation.
        """
        with patch('builtins.print') as mock_print:
            self.simulation.run()
            # Ensure each thread completes all stages
            for thread_id in range(3):
                for stage in range(1, 4):
                    mock_print.assert_any_call(f"\033[92mThread-{thread_id}: Starting stage {stage}\033[0m")
                    mock_print.assert_any_call(
                        f"\033[94mThread-{thread_id}: Waiting at barrier for stage {stage}\033[0m")
                    mock_print.assert_any_call(
                        f"\033[93mThread-{thread_id}: Passed barrier for stage {stage}\033[0m")

    def test_dynamic_configuration(self):
        """
        Test if the simulation adapts to dynamic configuration changes.
        """
        # Update configuration to test dynamic behavior
        self.simulation.config.data["num_threads"] = 2
        self.simulation.config.data["delay_between_stages"] = 0.5

        with patch('builtins.print') as mock_print:
            self.simulation.run()

        # Ensure two threads completed
        for thread_id in range(2):
            for stage in range(1, 4):
                mock_print.assert_any_call(f"\033[92mThread-{thread_id}: Starting stage {stage}\033[0m")

class TestMultiprocessingSimulation(unittest.TestCase):

    @patch('multiprocessing.Pool')
    def test_run_with_empty_arrays(self, MockPool):
        """
        Test multiprocessing simulation with arrays that should sum to zero.
        """
        # Mock the pool and worker function to avoid real multiprocessing
        mock_pool = MagicMock()
        MockPool.return_value = mock_pool
        mock_pool.map.return_value = [0, 0, 0, 0]

        sim = MultiprocessingSimulation()
        sim.config.data = {
            'array_size': 1000,
            'num_processes': 4,
            'num_arrays': 4
        }

        with patch('time.time', return_value=1):  # Mock time to avoid delays
            sim.run()

        # Test that all results are zero (because we mocked it)
        self.assertEqual(sum(mock_pool.map.return_value), 0)

    @patch('multiprocessing.Pool')
    def test_run_with_large_arrays(self, MockPool):
        """
        Test multiprocessing simulation with large arrays.
        """
        # Test with a large array size
        mock_pool = MagicMock()
        MockPool.return_value = mock_pool
        mock_pool.map.return_value = [np.random.random(1000000).sum() for _ in range(4)]

        sim = MultiprocessingSimulation()
        sim.config.data = {
            'array_size': 1000000,
            'num_processes': 4,
            'num_arrays': 4
        }

        with patch('time.time', return_value=1):  # Mock time to avoid delays
            sim.run()

        # Test that the results are correctly summed
        self.assertGreater(sum(mock_pool.map.return_value), 0)

    def test_worker(self):
        """
        Test the worker function of the multiprocessing simulation independently.
        """
        sim = MultiprocessingSimulation()
        array = np.array([1, 2, 3, 4, 5])
        result = sim.worker(array)
        self.assertEqual(result, 15)  # 1 + 2 + 3 + 4 + 5 = 15


class TestWordCountSimulation(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open,
           read_data="This is a default text for file creation. Use Python, multiprocessing, example.")
    def test_count_words_with_default_file(self, mock_file):
        """
        Test word counting functionality with a default file.
        """
        sim = WordCountSimulation()
        words_to_count = ["python", "multiprocessing", "example"]
        file_path = "test_file.txt"

        # Test word count logic
        result = sim.count_words(file_path, words_to_count)

        # Check if the count of each word is correct
        self.assertEqual(result["python"], 1)
        self.assertEqual(result["multiprocessing"], 1)
        self.assertEqual(result["example"], 1)

        # Check if file was opened correctly
        mock_file.assert_called_with(file_path, 'r')


class TestPrimeNumberSimulation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up test configurations for all PrimeNumberSimulation tests.
        """
        cls.test_config = Config()
        cls.test_config.data = {
            'start_number': 2,
            'end_number': 10,
            'num_processes': 2
        }

    def setUp(self):
        """
        Initialize the PrimeNumberSimulation instance for each test.
        """
        self.sim = PrimeNumberSimulation()
        self.sim.config = self.test_config  # Use our test config

    def test_is_prime(self):
        """
        Test the helper function for prime number checking.
        """
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertFalse(is_prime(4))
        self.assertTrue(is_prime(5))
        self.assertFalse(is_prime(6))
        self.assertTrue(is_prime(7))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(1))

    @patch('multiprocessing.Pool', autospec=True)
    def test_no_primes_found(self, mock_pool):
        """
        Test if the simulation correctly handles cases where no primes are found.
        """
        instance = mock_pool.return_value
        instance.starmap.return_value = [[], []]  # No primes in these ranges

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.sim.run()
            output = mock_stdout.getvalue()
            self.assertIn("Number of primes found: 0", output)
            self.assertIn("First 10 primes: []", output)

if __name__ == "__main__":
    unittest.main()