import cmd
import json

from config.config import Config
from examples.message import Messages
from examples.mp_calculation import MultiprocessingSimulation
from examples.mp_word_count import WordCountSimulation
from examples.prime_number_cal import PrimeNumberSimulation

from examples.shared_memory import SharedMemory
from color import Color
from examples.thread_synchronization import ThreadSynchronization

class InteractiveMenu(cmd.Cmd):
    intro = f"Welcome to the Thread Simulation Menu. Type help or ? to list commands."
    prompt = '(thread_sim) '

    def __init__(self):
        super().__init__()
        self.simulations = {
            'messages': Messages(),
            'shared_memory': SharedMemory(),
            'thread_synchronization': ThreadSynchronization(),
            'mp_array_calculation': MultiprocessingSimulation(),
            'word_count': WordCountSimulation(),
            'prime_numbers': PrimeNumberSimulation()
        }
        self.config = Config()
        if not self.config.get('use_colors', True):
            Color.RED = ''
            Color.GREEN = ''
            Color.BLUE = ''
            Color.RESET = ''
            Color.YELLOW = ''
        self.active_simulation = None

    def do_messages(self, arg):
        'Run or show code for the basic Messages simulation with threads: messages [run/show]'
        self._handle_command('messages', arg)

    def do_shared_memory(self, arg):
        'Run or show code for the Shared Memory simulation with threads: shared_memory [run/show]'
        self._handle_command('shared_memory', arg)

    def do_thread_synchronization(self, arg):
        'Run or show code for the Thread Synchronization simulation with threads: thread_synchronization [run/show]'
        self._handle_command('thread_synchronization', arg)

    def do_multiprocessing(self, arg):
        'Run or show code for multiprocessing calculation simulation: multiprocessing [run/show]'
        self._handle_command('mp_array_calculation', arg)

    def do_word_count(self, arg):
        'Run or show code for Word Count simulation: word_count [run/show]'
        self._handle_command('word_count', arg)

    def do_prime_numbers(self, arg):
        'Run or show code for Prime Number simulation: prime_numbers [run/show]'
        self._handle_command('prime_numbers', arg)

    def _handle_command(self, simulation_name, arg):
        simulation = self.simulations.get(simulation_name)
        if not simulation:
            print(f"{Color.RED}Simulation '{simulation_name}' not found.{Color.RESET}")
            return

        if arg.lower() == 'run':
            simulation.run()
        elif arg.lower() == 'show':
            simulation.show_code()
        else:
            print(f"{Color.RED}Invalid command. Use 'run' or 'show'.{Color.RESET}")

    def do_exit(self, arg):
        'Exit the simulation menu'
        print(f"{Color.GREEN}Exiting...{Color.RESET}")
        return True

    def do_EOF(self, arg):
        'Handle end of file (Ctrl-D)'
        print(f"{Color.GREEN}Exiting...{Color.RESET}")
        return True

    def do_config(self, arg):
        'View or set configuration: config [key] [value]'
        args = arg.split()
        if not args:
            self._show_all_config()
        elif len(args) == 1:
            self._show_config(args[0])
        elif len(args) == 2:
            self._set_config(args[0], args[1])
        else:
            print("Usage: config [key] [value] or config to view all configs")

    def _show_all_config(self):
        for key, value in self.config.data.items():
            print(f"{key}: {value}")

    def _show_config(self, key):
        value = self.config.get(key)
        if value is not None:
            print(f"{key}: {value}")
        else:
            print(f"Configuration key '{key}' not found.")

    def _set_config(self, key, value):
        try:
            current_type = type(self.config.get(key, ''))
            if current_type is bool:
                value = value.lower() in ('true', 'yes', 'on', '1')
            elif current_type in (int, float):
                value = current_type(value)
            self.config.data[key] = value
            # Write back to the config file
            with open('config.json', 'w') as f:
                json.dump(self.config.data, f, indent=4)
            print(f"Configuration updated: {key} = {value}")
            for simulations in self.simulations.values():
                simulations.config = self.config
        except ValueError:
            print(f"Error: Invalid value for {key}. Expected type {current_type.__name__}")

if __name__ == '__main__':
    InteractiveMenu().cmdloop()