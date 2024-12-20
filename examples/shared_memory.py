import threading
import time
from abc import ABC, abstractmethod
from color import Color
from config.config import Config
from examples.simulation import Simulation



class SharedMemory(Simulation):
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()
        self.config = Config()
        self.max_threads = self.config.get('max_threads', 10)

    def increment(self, thread_name):
        for _ in range(100000):
            with self.lock:
                self.counter += 1
            if _ % 10000 == 0:
                time.sleep(self.config.get('delay_between_messages', 2))
                print(f"{Color.GREEN}{thread_name}: Counter is now {self.counter}{Color.RESET}")
                print(f"{Color.BLUE}Blueprint: Both threads are trying to add to the same bank account, but only one can do it at a time.{Color.RESET}")

    def run(self):
        print(f"{Color.BLUE}Blueprint: Here, we're showing how threads can safely share and modify memory using locks to avoid race conditions.{Color.RESET}")
        threads = []
        for i in range(self.max_threads):
            t = threading.Thread(target=self.increment, args=(f"Thread-{i}",))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        time.sleep(self.config.get('delay_between_messages', 2))
        print(f"{Color.RED}Final counter value: {self.counter}{Color.RESET}")
        print(f"Expected count if no race condition: {self.max_threads*100000}")

    def show_code(self):
        print("""
        import threading
        import time

        class SharedMemory(Simulation):
            def __init__(self):
                self.counter = 0
                self.lock = threading.Lock()
        
            def increment(self, thread_name):
                for _ in range(100000):
                    with self.lock:
                        self.counter += 1
                    if _ % 10000 == 0:
                        time.sleep(1)
                        print(f"{Color.GREEN}{thread_name}: Counter is now {self.counter}{Color.RESET}")
                        print(f"{Color.BLUE}Blueprint: Both threads are trying to add to the same bank account, but only one can do it at a time.{Color.RESET}")
        
            def run(self):
                print(f"{Color.BLUE}Blueprint: Here, we're showing how threads can safely share and modify memory using locks to avoid race conditions.{Color.RESET}")
                threads = [
                    threading.Thread(target=self.increment, args=("Thread-1",)),
                    threading.Thread(target=self.increment, args=("Thread-2",))
                ]
        
                for thread in threads:
                    thread.start()
        
                for thread in threads:
                    thread.join()
        
                time.sleep(2)
                print(f"{Color.RED}Final counter value: {self.counter}{Color.RESET}")
                print(f"Expected count if no race condition: {200000}")

        """)