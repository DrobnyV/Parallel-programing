import threading
import time
from color import Color
from config.config import Config
from examples.simulation import Simulation



class SharedMemory(Simulation):
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()
        self.config = Config()
        self.max_threads = self.config.get('max_threads', 10)
        self.print_lock = threading.Lock()

    def increment(self, thread_name):
        """
        Increment the shared counter in a thread-safe manner.

        Each thread attempts to increase the counter, using a lock to ensure
        atomicity of the operation, thus avoiding race conditions.

        :param thread_name: Name of the thread for identification in print statements.
        """
        for _ in range(100000):
            with self.lock:
                self.counter += 1
            if _ % 10000 == 0:
                time.sleep(self.config.get('delay_between_messages', 2))
                with self.print_lock:
                    print(f"{Color.GREEN}{thread_name}: Counter is now {self.counter}{Color.RESET}")
                    print(f"{Color.BLUE}Blueprint: Every thread is trying to add to the same bank account, but only one can do it at a time.{Color.RESET}")

    def run(self):
        """
        Run the simulation where multiple threads concurrently increment a shared counter.

        This method creates and manages threads, ensuring synchronized access to
        shared memory to demonstrate lock usage for thread safety.
        """
        with self.print_lock:
            print(f"{Color.BLUE}Blueprint: Here, we're showing how threads can safely share and modify memory using locks to avoid race conditions.{Color.RESET}")
        threads = []
        for i in range(self.max_threads):
            t = threading.Thread(target=self.increment, args=(f"Thread-{i}",))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        time.sleep(self.config.get('delay_between_messages', 2))
        with self.print_lock:
            print(f"{Color.RED}Final counter value: {self.counter}{Color.RESET}")
            print(f"Expected count if no race condition: {self.max_threads*100000}")

    def show_code(self):
        """
        Displays the code of a simplified SharedMemory simulation for educational purposes.
        """
        print("""
        import threading
        import time
        from color import Color
        from config.config import Config
        from examples.simulation import Simulation
        
        
        
        class SharedMemory(Simulation):
            def __init__(self):
                self.counter = 0
                self.lock = threading.Lock()
                self.config = Config()
                self.max_threads = self.config.get('max_threads', 10)
                self.print_lock = threading.Lock()
        
            def increment(self, thread_name):
                
                for _ in range(100000):
                    with self.lock:
                        self.counter += 1
                    if _ % 10000 == 0:
                        time.sleep(self.config.get('delay_between_messages', 2))
                        with self.print_lock:
                            print(f"{Color.GREEN}{thread_name}: Counter is now {self.counter}{Color.RESET}")
                            print(f"{Color.BLUE}Blueprint: Every thread is trying to add to the same bank account, but only one can do it at a time.{Color.RESET}")
        
            def run(self):
                
                with self.print_lock:
                    print(f"{Color.BLUE}Blueprint: Here, we're showing how threads can safely share and modify memory using locks to avoid race conditions.{Color.RESET}")
                threads = []
                for i in range(self.max_threads):
                    t = threading.Thread(target=self.increment, args=(f"Thread-{i}",))
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()
        
                time.sleep(self.config.get('delay_between_messages', 2))
                with self.print_lock:
                    print(f"{Color.RED}Final counter value: {self.counter}{Color.RESET}")
                    print(f"Expected count if no race condition: {self.max_threads*100000}")

        """)