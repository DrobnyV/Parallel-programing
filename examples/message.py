import threading
import time
from abc import ABC, abstractmethod
import queue
from color import Color
from examples.simulation import Simulation


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