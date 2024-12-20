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
        self.print_lock = threading.Lock()

    def producer(self):
        """
        Produces messages and puts them into the queue.
        Simulates a delay between each message to mimic real-world scenarios.

        This method prints the status of each message sent, using a lock to avoid
        overlapping output from different threads.
        """
        for i in range(self.config.get('message_count', 5)):
            time.sleep(self.config.get('delay_between_messages', 2))
            self.message_queue.put(f"Message {i}")
            with self.print_lock:
                print(f"{Color.GREEN}Producer: Sent message {i}{Color.RESET}")
                print(
                    f"{Color.BLUE}Blueprint: Imagine the producer as a chef sending dishes to a kitchen window.{Color.RESET}")

    def consumer(self):
        """
        Consumes messages from the queue.
        It waits for messages with a timeout, simulating a consumer that might
        need to wait for production.

        Prints each message received and uses a lock for thread-safe printing.
        """
        consumed_count = 0
        while consumed_count < self.config.get('message_count', 5):
            try:
                message = self.message_queue.get(block=True, timeout=5)  # Wait for up to 5 seconds for a message
                time.sleep(self.config.get('delay_between_messages', 2))
                with self.print_lock:
                    print(f"{Color.RED}Consumer: Received {message}{Color.RESET}")
                    print(
                        f"{Color.BLUE}Blueprint: The consumer is like a waiter picking up dishes from the window.{Color.RESET}")
                self.message_queue.task_done()
                consumed_count += 1
            except queue.Empty:
                with self.print_lock:
                    print(f"{Color.RED}Consumer: No message available, waiting...{Color.RESET}")
                continue

    def run(self):
        """
        Runs the simulation by starting both producer and consumer threads.

        The producer is started first to populate the queue before the consumer
        starts, ensuring there are messages to consume.
        """
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
        """
        Displays the code of a simplified Messages simulation for educational purposes.
        """
        print("""
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
                self.print_lock = threading.Lock()
        
            def producer(self):
                for i in range(self.config.get('message_count', 5)):
                    time.sleep(self.config.get('delay_between_messages', 2))
                    self.message_queue.put(f"Message {i}")
                    with self.print_lock:
                        print(f"{Color.GREEN}Producer: Sent message {i}{Color.RESET}")
                        print(
                            f"{Color.BLUE}Blueprint: Imagine the producer as a chef sending dishes to a kitchen window.{Color.RESET}")
        
            def consumer(self):
                consumed_count = 0
                while consumed_count < self.config.get('message_count', 5):
                    try:
                        message = self.message_queue.get(block=True, timeout=5)
                        time.sleep(self.config.get('delay_between_messages', 2))
                        with self.print_lock:
                            print(f"{Color.RED}Consumer: Received {message}{Color.RESET}")
                            print(
                                f"{Color.BLUE}Blueprint: The consumer is like a waiter picking up dishes from the window.{Color.RESET}")
                        self.message_queue.task_done()
                        consumed_count += 1
                    except queue.Empty:
                        with self.print_lock:
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
        """)