import threading
import time
from color import Color
from config.config import Config
from examples.simulation import Simulation


class ThreadSynchronization(Simulation):
    def __init__(self):
        self.config = Config()
        self.num_threads = self.config.get('num_threads', 5)
        self.barrier = threading.Barrier(self.num_threads)
        self.print_lock = threading.Lock()  # Ensure thread-safe printing

    def worker(self, thread_id):
        """
        Perform work in stages, waiting at barriers between each stage.

        This method simulates each thread doing some work, then waiting
        for all threads to reach the same point before proceeding.

        :param thread_id: An identifier for the thread, used in print statements.
        """
        try:
            for stage in range(1, 4):  # Three stages of processing
                with self.print_lock:
                    print(f"{Color.GREEN}Thread-{thread_id}: Starting stage {stage}{Color.RESET}")

                time.sleep(self.config.get('delay_between_stages', 1))  # Simulate work

                with self.print_lock:
                    print(f"{Color.BLUE}Thread-{thread_id}: Waiting at barrier for stage {stage}{Color.RESET}")

                self.barrier.wait()  # Synchronize threads at the barrier

                with self.print_lock:
                    print(f"{Color.YELLOW}Thread-{thread_id}: Passed barrier for stage {stage}{Color.RESET}")
        except threading.BrokenBarrierError:
            with self.print_lock:
                print(f"{Color.RED}Thread-{thread_id}: Barrier broken. Exiting.{Color.RESET}")

    def run(self):
        """
        Run the simulation where threads synchronize at barriers.

        This method creates threads that each execute the `worker` method,
        demonstrating thread synchronization through barriers.
        """
        with self.print_lock:
            print(
                f"{Color.BLUE}Blueprint: Threads will perform tasks in stages, synchronizing at barriers before moving to the next stage.{Color.RESET}")

        threads = []
        for i in range(self.num_threads):
            t = threading.Thread(target=self.worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        with self.print_lock:
            print(f"{Color.GREEN}All threads completed their tasks.{Color.RESET}")

    def show_code(self):
        """
        Displays the code of a simplified ThreadSynchronization simulation for educational purposes.
        """
        print("""
        import threading
        import time
        from color import Color
        from config.config import Config
        from examples.simulation import Simulation
        
        
        class ThreadSynchronization(Simulation):
            def __init__(self):
                self.config = Config()
                self.num_threads = self.config.get('num_threads', 5)
                self.barrier = threading.Barrier(self.num_threads)
                self.print_lock = threading.Lock()  # Ensure thread-safe printing
        
            def worker(self, thread_id):
                
                try:
                    for stage in range(1, 4):  # Three stages of processing
                        with self.print_lock:
                            print(f"{Color.GREEN}Thread-{thread_id}: Starting stage {stage}{Color.RESET}")
        
                        time.sleep(self.config.get('delay_between_stages', 1))  # Simulate work
        
                        with self.print_lock:
                            print(f"{Color.BLUE}Thread-{thread_id}: Waiting at barrier for stage {stage}{Color.RESET}")
        
                        self.barrier.wait()  # Synchronize threads at the barrier
        
                        with self.print_lock:
                            print(f"{Color.YELLOW}Thread-{thread_id}: Passed barrier for stage {stage}{Color.RESET}")
                except threading.BrokenBarrierError:
                    with self.print_lock:
                        print(f"{Color.RED}Thread-{thread_id}: Barrier broken. Exiting.{Color.RESET}")
        
            def run(self):
               
                with self.print_lock:
                    print(
                        f"{Color.BLUE}Blueprint: Threads will perform tasks in stages, synchronizing at barriers before moving to the next stage.{Color.RESET}")
        
                threads = []
                for i in range(self.num_threads):
                    t = threading.Thread(target=self.worker, args=(i,))
                    threads.append(t)
                    t.start()
        
                for t in threads:
                    t.join()
        
                with self.print_lock:
                    print(f"{Color.GREEN}All threads completed their tasks.{Color.RESET}")

        """)

