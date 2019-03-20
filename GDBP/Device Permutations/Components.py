class Component:
    def __init__(self, ID, cost, volume, quantity):
        self.ID = ID
        self.cost = cost
        self.volume = volume
        self.quantity = quantity


class Permutations:
    def __init__(self, ID, components, cost, volume):
        self.ID = ID
        self.components = components
        self.cost = cost
        self.volume = volume
