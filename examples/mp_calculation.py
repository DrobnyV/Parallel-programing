# examples/multiprocessing_simulation.py

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
        """Worker function to sum up an array."""
        return np.sum(array)

    def run(self):
        array_size = self.config.get('array_size', 1000000)
        num_processes = self.config.get('num_processes', 4)
        num_arrays = self.config.get('num_arrays', 4)

        # Generate arrays
        arrays = [np.random.random(array_size) for _ in range(num_arrays)]

        # Multiprocessing setup
        with multiprocessing.Pool(processes=num_processes) as pool:
            start_time = time()
            results = pool.map(self.worker, arrays)
            end_time = time()

        # Print results
        print(f"{Color.BLUE}Blueprint: This simulation demonstrates how multiprocessing can parallelize CPU-intensive tasks across multiple cores.{Color.RESET}")
        print(f"{Color.GREEN}Multiprocessing Results:")
        print(f"- Number of processes used: {num_processes}")
        print(f"- Array size per process: {array_size}")
        print(f"- Number of arrays: {num_arrays}")
        print(f"- Total sum of arrays: {sum(results)}")
        print(f"- Time taken: {end_time - start_time:.4f} seconds{Color.RESET}")

    def show_code(self):
        print("""
        class MultiprocessingSimulation(Simulation):
    def __init__(self):
        self.config = Config()

    def worker(self, array):
        return np.sum(array)

    def run(self):
        array_size = self.config.get('array_size', 1000000)
        num_processes = self.config.get('num_processes', 4)
        num_arrays = self.config.get('num_arrays', 4)

        # Generate arrays
        arrays = [np.random.random(array_size) for _ in range(num_arrays)]

        # Multiprocessing setup
        with multiprocessing.Pool(processes=num_processes) as pool:
            start_time = time()
            results = pool.map(self.worker, arrays)
            end_time = time()

        # Print results
        print(f"{Color.BLUE}Blueprint: This simulation demonstrates how multiprocessing can parallelize CPU-intensive tasks across multiple cores.{Color.RESET}")
        print(f"{Color.GREEN}Multiprocessing Results:")
        print(f"- Number of processes used: {num_processes}")
        print(f"- Array size per process: {array_size}")
        print(f"- Number of arrays: {num_arrays}")
        print(f"- Total sum of arrays: {sum(results)}")
        print(f"- Time taken: {end_time - start_time:.4f} seconds{Color.RESET}")
        """)  # Placeholder for showing code if needed

if __name__ == '__main__':
    sim = MultiprocessingSimulation()
    sim.run()