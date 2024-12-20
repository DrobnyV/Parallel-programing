import threading
import time
import queue
from color import Color
from config.config import Config
from examples.simulation import Simulation


class Messages(Simulation):
    def __init__(self):
        self.message_queue = queue.Queue()
        self.config = Config()

    def producer(self):
        for i in range(self.config.get('message_count', 5)):
            time.sleep(self.config.get('delay_between_messages', 2))
            self.message_queue.put(f"Message {i}")
            print(f"{Color.GREEN}Producer: Sent message {i}{Color.RESET}")
            print(
                f"{Color.BLUE}Blueprint: Imagine the producer as a chef sending dishes to a kitchen window.{Color.RESET}")

    def consumer(self):
        consumed_count = 0
        while consumed_count < self.config.get('message_count', 5):
            try:
                message = self.message_queue.get(block=True, timeout=5)  # Wait for up to 5 seconds for a message
                time.sleep(self.config.get('delay_between_messages', 2))
                print(f"{Color.RED}Consumer: Received {message}{Color.RESET}")
                print(
                    f"{Color.BLUE}Blueprint: The consumer is like a waiter picking up dishes from the window.{Color.RESET}")
                self.message_queue.task_done()
                consumed_count += 1
            except queue.Empty:
                print(f"{Color.RED}Consumer: No message available, waiting...{Color.RESET}")
                continue

    def run(self):
        print(
            f"{Color.BLUE}Blueprint: This simulation demonstrates message passing between threads using a queue.{Color.RESET}")

        # Start producer first to ensure messages are in the queue before consumer starts
        producer_thread = threading.Thread(target=self.producer)
        producer_thread.start()

        consumer_thread = threading.Thread(target=self.consumer)
        consumer_thread.start()

        producer_thread.join()  # Wait for producer to finish before consumer can potentially end
        consumer_thread.join()

    def show_code(self):
        print("""
        import threading
        import time
        import queue

        class Messages(Simulation):
            def __init__(self):
                self.message_queue = queue.Queue()
        
            def producer(self):
                for i in range(5):
                    time.sleep(2)
                    self.message_queue.put(f"Message {i}")
                    print(f"{Color.GREEN}Producer: Sent message {i}{Color.RESET}")
                    print(
                        f"{Color.BLUE}Blueprint: Imagine the producer as a chef sending dishes to a kitchen window.{Color.RESET}")
        
            def consumer(self):
                for i in range(5):
                    message = self.message_queue.get()
                    time.sleep(2) 
                    print(f"{Color.RED}Consumer: Received {message}{Color.RESET}")
                    print(
                        f"{Color.BLUE}Blueprint: The consumer is like a waiter picking up dishes from the window.{Color.RESET}")
                    self.message_queue.task_done()
        
            def run(self):
                print(
                    f"{Color.BLUE}Blueprint: This simulation demonstrates message passing between threads using a queue.{Color.RESET}")
                threads = [
                    threading.Thread(target=self.producer),
                    threading.Thread(target=self.consumer)
                ]
        
                for thread in threads:
                    thread.start()
        
                for thread in threads:
                    thread.join()
        """)