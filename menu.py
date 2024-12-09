from examples.message import Messages


class Menu:
    def __init__(self):
        self.simulations = {
            1: Messages()

        }
    @staticmethod
    def is_convertible_to_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def display(self):
        print("Choose:")
        for key, sim in self.simulations.items():
            print(f"{key}. {sim.__class__.__name__}")

    def run(self):
        while True:
            self.display()
            choice = input("Your choice: ")
            if Menu.is_convertible_to_int(choice):
                choice = int(choice)
                simulation = self.simulations.get(choice)
                if simulation:
                    print("1: Show code ")
                    print("2: Run simulation")
                    subchoice = input("Your choice: ")
                    if Menu.is_convertible_to_int(subchoice):
                        subchoice = int(subchoice)
                        Menu.is_convertible_to_int(subchoice)
                        if subchoice == 1:
                            simulation.show_code()
                        elif subchoice == 2:
                            simulation.run()
                        else:
                            print("Wrong choice!")
                    else: print("Input must be integer")
                else:
                    print("Wrong choice!")
            else:
                print("Input must be integer!")