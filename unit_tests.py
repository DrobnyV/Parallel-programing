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

    def test_run_messages_simulation(self):
        with patch.object(Messages, 'run', return_value=None) as mock_run:
            self.menu.do_messages('run')
            mock_run.assert_called_once()

    def test_show_shared_memory_code(self):
        with patch.object(SharedMemory, 'show_code', return_value=None) as mock_show_code:
            self.menu.do_shared_memory('show')
            mock_show_code.assert_called_once()

    def test_config_set_and_get(self):
        self.menu.do_config('test_key 42')
        self.assertEqual(self.menu.config.get('test_key'), '42')

if __name__ == "__main__":
    unittest.main()
