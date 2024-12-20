import cmd
from abc import ABC, abstractmethod
from examples.message import Messages
from examples.shared_memory import SharedMemory
from color import Color

class InteractiveMenu(cmd.Cmd):
    intro = f"{Color.BLUE}Welcome to the Thread Simulation Menu. Type help or ? to list commands.{Color.RESET}"
    prompt = '(thread_sim) '

    def __init__(self):
        super().__init__()
        self.simulations = {
            'messages': Messages(),
            'shared_memory': SharedMemory()
        }

    def do_messages(self, arg):
        'Run or show code for the basic Messages simulation: messages [run/show]'
        self._handle_command('messages', arg)

    def do_shared_memory(self, arg):
        'Run or show code for the Shared Memory simulation: shared_memory [run/show]'
        self._handle_command('shared_memory', arg)

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

    def do_exit(self):
        'Exit the simulation menu'
        print(f"{Color.GREEN}Exiting...{Color.RESET}")
        return True

    def do_EOF(self):
        'Handle end of file (Ctrl-D)'
        print(f"{Color.GREEN}Exiting...{Color.RESET}")
        return True

if __name__ == '__main__':
    InteractiveMenu().cmdloop()