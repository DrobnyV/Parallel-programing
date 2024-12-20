import multiprocessing
import numpy as np
from time import time
from color import Color
from config.config import Config
from examples.simulation import Simulation


class MultiprocessingSimulation(Simulation):
    def __init__(self):
        self.config = Config()

    def worker(self, array):
        """
        Worker function to compute the sum of an array.

        :param array: A NumPy array to sum.
        :return: The sum of the array elements.
        """
        return np.sum(array)

    def run(self):
        """
        Runs the multiprocessing simulation for summing large arrays.

        This method generates arrays, uses multiprocessing to sum them in parallel,
        and then prints the results including performance metrics.
        """
        array_size = self.config.get('array_size', 1000000)
        num_processes = self.config.get('num_processes', 4)
        num_arrays = self.config.get('num_arrays', 4)

        arrays = [np.random.random(array_size) for _ in range(num_arrays)]

        with multiprocessing.Pool(processes=num_processes) as pool:
            start_time = time()
            results = pool.map(self.worker, arrays)
            end_time = time()

        print(
            f"{Color.BLUE}Blueprint: This simulation demonstrates how multiprocessing can parallelize CPU-intensive tasks across multiple cores.{Color.RESET}")
        print(f"{Color.GREEN}Multiprocessing Results:")
        print(f"- Number of processes used: {num_processes}")
        print(f"- Array size per process: {array_size}")
        print(f"- Number of arrays: {num_arrays}")
        print(f"- Total sum of arrays: {sum(results)}")
        print(f"- Time taken: {end_time - start_time:.4f} seconds{Color.RESET}")

    def show_code(self):
        """
        Displays the code of the MultiprocessingSimulation for educational purposes.
        """
        print("""
        import multiprocessing
        import numpy as np
        from time import time
        from color import Color
        from config.config import Config
        from examples.simulation import Simulation

        class MultiprocessingSimulation(Simulation):
            def __init__(self):
                self.config = Config()

            def worker(self, array):
                return np.sum(array)

            def run(self):
                array_size = self.config.get('array_size', 1000000)
                num_processes = self.config.get('num_processes', 4)
                num_arrays = self.config.get('num_arrays', 4)


                arrays = [np.random.random(array_size) for _ in range(num_arrays)]


                with multiprocessing.Pool(processes=num_processes) as pool:
                    start_time = time()
                    results = pool.map(self.worker, arrays)
                    end_time = time()


                print(f"{Color.BLUE}Blueprint: This simulation demonstrates how multiprocessing can parallelize CPU-intensive tasks across multiple cores.{Color.RESET}")
                print(f"{Color.GREEN}Multiprocessing Results:")
                print(f"- Number of processes used: {num_processes}")
                print(f"- Array size per process: {array_size}")
                print(f"- Number of arrays: {num_arrays}")
                print(f"- Total sum of arrays: {sum(results)}")
                print(f"- Time taken: {end_time - start_time:.4f} seconds{Color.RESET}")
        """)


if __name__ == '__main__':
    sim = MultiprocessingSimulation()
    sim.run()