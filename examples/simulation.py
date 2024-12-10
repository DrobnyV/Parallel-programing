from abc import ABC


class Simulation(ABC):
    def run(self):
        raise NotImplemented
    def show_code(self):
        raise NotImplemented
