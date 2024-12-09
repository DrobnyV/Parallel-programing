class Menu:
    def __init__(self):
        self.simulations = {

        }
    @staticmethod
    def check_if_int(input):
        if type(input) != int:
            raise TypeError("Input must be an integer")

    def display(self):
        print("Choose:")
        for key, sim in self.simulations.items():
            print(f"{key}. {sim.__class__.__name__}")

    def run(self):
        while True:
            self.display()
            choice = input("Your choice: ")
            Menu.check_if_int(choice)
            simulation = self.simulations.get(choice)
            if simulation:
                print("1: Show code ")
                print("2: Run simulation")
                subchoice = input("Your choice: ")
                Menu.check_if_int(subchoice)
                if subchoice == 1:
                    simulation.show_code()
                elif subchoice == 2:
                    simulation.run()
                else:
                    print("Wrong choice!")
            else:
                print("Wrong choice!")