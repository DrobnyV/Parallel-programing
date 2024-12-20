import multiprocessing
from collections import Counter
from time import time
from color import Color
from config.config import Config
from examples.simulation import Simulation
import os


class WordCountSimulation(Simulation):
    def __init__(self):
        self.config = Config()

    def count_words(self, file_path, words_to_count):
        """
        Count specified words in a single file. If the file doesn't exist,
        it creates a default file with sample content.

        :param file_path: Path to the file to be processed.
        :param words_to_count: List of words to count in the file.
        :return: Dictionary with words and their counts.
        """
        try:
            with open(file_path, 'r') as file:
                text = file.read().lower()
        except FileNotFoundError:
            with open(file_path, 'w') as file:
                file.write("This is a default text for file creation. Use Python, multiprocessing, example.")
            with open(file_path, 'r') as file:
                text = file.read().lower()
        counts = {word: text.count(word) for word in words_to_count}
        return counts

    def run(self):
        """
        Runs the word count simulation using multiprocessing to handle multiple files.

        This method checks for file existence, creates missing files, processes
        them in parallel, and prints the results.
        """
        num_files = self.config.get('num_files', 5)
        num_processes = self.config.get('num_processes', 4)
        words_to_count = self.config.get('words_to_count', ["python", "multiprocessing", "example"])
        file_prefix = self.config.get('file_prefix', "text")

        file_paths = []
        for i in range(num_files):
            file_name = f"{file_prefix}_{i}.txt"
            if not os.path.exists(file_name):
                print(f"{Color.YELLOW}File {file_name} not found. Creating default file.{Color.RESET}")
                with open(file_name, 'w') as file:
                    file.write("This is a default text for file creation. Use Python, multiprocessing, example.")
            file_paths.append(file_name)

        start_time = time()
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.starmap(self.count_words, [(path, words_to_count) for path in file_paths])

        end_time = time()

        total_counts = Counter()
        for counts in results:
            total_counts.update(counts)

        print(
            f"{Color.BLUE}Blueprint: This simulation demonstrates how multiprocessing can handle both I/O and CPU-bound tasks by counting words across multiple files.{Color.RESET}")
        print(f"{Color.GREEN}Word Count Results:")
        print(f"- Number of processes used: {num_processes}")
        print(f"- Number of files processed: {num_files}")
        print(f"- Words counted: {', '.join(words_to_count)}")
        print(f"- Time taken: {end_time - start_time:.4f} seconds{Color.RESET}")
        for word, count in total_counts.items():
            print(f"  - {word}: {count}")

    def show_code(self):
        """
        Displays the code of the WordCountSimulation for educational purposes.
        """
        print("""
        import multiprocessing
        from collections import Counter
        from time import time
        from color import Color
        from config.config import Config
        from examples.simulation import Simulation
        import os

        class WordCountSimulation(Simulation):
            def __init__(self):
                self.config = Config()

            def count_words(self, file_path, words_to_count):
                try:
                    with open(file_path, 'r') as file:
                        text = file.read().lower()
                except FileNotFoundError:
                    with open(file_path, 'w') as file:
                        file.write("This is a default text for file creation. Use Python, multiprocessing, example.")
                    with open(file_path, 'r') as file:
                        text = file.read().lower()
                counts = {word: text.count(word) for word in words_to_count}
                return counts

            def run(self):
                num_files = self.config.get('num_files', 5)
                num_processes = self.config.get('num_processes', 4)
                words_to_count = self.config.get('words_to_count', ["python", "multiprocessing", "example"])
                file_prefix = self.config.get('file_prefix', "text")

                file_paths = []
                for i in range(num_files):
                    file_name = f"{file_prefix}_{i}.txt"
                    if not os.path.exists(file_name):
                        print(f"{Color.YELLOW}File {file_name} not found. Creating default file.{Color.RESET}")
                        with open(file_name, 'w') as file:
                            file.write("This is a default text for file creation. Use Python, multiprocessing, example.")
                    file_paths.append(file_name)

                start_time = time()
                with multiprocessing.Pool(processes=num_processes) as pool:
                    results = pool.starmap(self.count_words, [(path, words_to_count) for path in file_paths])

                end_time = time()

                total_counts = Counter()
                for counts in results:
                    total_counts.update(counts)

                print(f"{Color.BLUE}Blueprint: This simulation demonstrates how multiprocessing can handle both I/O and CPU-bound tasks by counting words across multiple files.{Color.RESET}")
                print(f"{Color.GREEN}Word Count Results:")
                print(f"- Number of processes used: {num_processes}")
                print(f"- Number of files processed: {num_files}")
                print(f"- Words counted: {', '.join(words_to_count)}")
                print(f"- Time taken: {end_time - start_time:.4f} seconds{Color.RESET}")
                for word, count in total_counts.items():
                    print(f"  - {word}: {count}")
        """)