import multiprocessing
from time import time
from color import Color
from config.config import Config
from examples.simulation import Simulation


def is_prime(n):
    """
    Check if a number is prime.

    :param n: The number to check for primality.
    :return: True if the number is prime, False otherwise.
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


class PrimeNumberSimulation(Simulation):
    def __init__(self):
        self.config = Config()

    def worker(self, start, end):
        """
        Find prime numbers within a given range.

        :param start: The start of the range to check.
        :param end: The end of the range to check.
        :return: List of prime numbers found within the range.
        """
        primes = [num for num in range(start, end) if is_prime(num)]
        return primes

    def run(self):
        """
        Runs the prime number simulation using multiprocessing to check for primes in parallel.

        This method divides the range among processes, computes primes,
        and then prints the results including performance metrics.
        """
        start_number = self.config.get('start_number', 2)
        end_number = self.config.get('end_number', 100000)
        num_processes = self.config.get('num_processes', 4)


        chunk_size = (end_number - start_number + 1) // num_processes
        ranges = [(start_number + i * chunk_size, start_number + (i + 1) * chunk_size)
                  for i in range(num_processes)]

        ranges[-1] = (ranges[-1][0], end_number + 1)

        start_time = time()
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.starmap(self.worker, ranges)

        end_time = time()


        all_primes = [prime for sublist in results for prime in sublist]

        print(
            f"{Color.BLUE}Blueprint: This simulation demonstrates how multiprocessing can be used to distribute CPU-intensive tasks like prime number computation.{Color.RESET}")
        print(f"{Color.GREEN}Prime Number Calculation Results:")
        print(f"- Number of processes used: {num_processes}")
        print(f"- Range checked: {start_number} to {end_number}")
        print(f"- Number of primes found: {len(all_primes)}")
        print(f"- Time taken: {end_time - start_time:.4f} seconds{Color.RESET}")
        # Print first few primes for demonstration
        print(f"First 10 primes: {all_primes[:10]}")

    def show_code(self):
        """
        Displays the code of the PrimeNumberSimulation for educational purposes.
        """
        print("""
        import multiprocessing
        from time import time
        from color import Color
        from config.config import Config
        from examples.simulation import Simulation

        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True

        class PrimeNumberSimulation(Simulation):
            def __init__(self):
                self.config = Config()

            def worker(self, start, end):
                primes = [num for num in range(start, end) if is_prime(num)]
                return primes

            def run(self):
                start_number = self.config.get('start_number', 2)
                end_number = self.config.get('end_number', 100000)
                num_processes = self.config.get('num_processes', 4)

                
                chunk_size = (end_number - start_number + 1) // num_processes
                ranges = [(start_number + i * chunk_size, start_number + (i + 1) * chunk_size)
                          for i in range(num_processes)]
                
                ranges[-1] = (ranges[-1][0], end_number + 1)

                start_time = time()
                with multiprocessing.Pool(processes=num_processes) as pool:
                    results = pool.starmap(self.worker, ranges)

                end_time = time()

                
                all_primes = [prime for sublist in results for prime in sublist]

                print(
                    f"{Color.BLUE}Blueprint: This simulation demonstrates how multiprocessing can be used to distribute CPU-intensive tasks like prime number computation.{Color.RESET}")
                print(f"{Color.GREEN}Prime Number Calculation Results:")
                print(f"- Number of processes used: {num_processes}")
                print(f"- Range checked: {start_number} to {end_number}")
                print(f"- Number of primes found: {len(all_primes)}")
                print(f"- Time taken: {end_time - start_time:.4f} seconds{Color.RESET}")
                # Print first few primes for demonstration
                print(f"First 10 primes: {all_primes[:10]}")
        """)