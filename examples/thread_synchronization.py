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

    def show_code(self):
        print("""
        import threading
        import time

        class ThreadSynchronization(Simulation):
            def __init__(self):
                self.config = Config()
                self.num_threads = self.config.get('num_threads', 5)
                self.barrier = threading.Barrier(self.num_threads)

            def worker(self, thread_id):
                try:
                    for stage in range(1, 4):
                        print(f"Thread-{thread_id}: Starting stage {stage}")
                        time.sleep(1)
                        self.barrier.wait()
                        print(f"Thread-{thread_id}: Passed barrier for stage {stage}")
                except threading.BrokenBarrierError:
                    print(f"Thread-{thread_id}: Barrier broken. Exiting.")

            def run(self):
                threads = []
                for i in range(self.num_threads):
                    t = threading.Thread(target=self.worker, args=(i,))
                    threads.append(t)
                    t.start()

                for t in threads:
                    t.join()

        """)

