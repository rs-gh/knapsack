from abc import ABC, abstractmethod
from utils import debug_print


class KnapsackSolver(ABC):
    def __init__(self, items, capacity, item_count, ks_index, order, debug, epsilon=0):
        if order == "descending_value_density":
            self.items = Solver.value_density_order(items, desc=True)
        elif order == "ascending_value_density":
            self.items = Solver.value_density_order(items)
        elif order == "descending_weight":
            self.items = Solver.weight_order(items, desc=True)
        elif order == "ascending_weight":
            self.items = Solver.weight_order(items)
        else:
            self.items = items
        debug_print("ordered items: {}".format(self.items), debug=debug)
        self.capacity = capacity
        self.item_count = item_count
        self.ks_index = ks_index
        self.value = None
        self.debug = debug
        self.picked_items = []
        self.picked_items_assignment = [0] * self.item_count
        self.epsilon = 0
        self.cache = {}


    @staticmethod
    def value_density_order(items, desc=False):
        return sorted(items, key=lambda item: item.value/item.weight, reverse=desc)


    @staticmethod
    def weight_order(items, desc=False):
        return sorted(items, key=lambda item: item.weight, reverse=desc)


    @abstractmethod
    def solve(self, *args, **kwargs):
        pass


    def get_picked_items_assignment(self):
        for i in self.picked_items:
            self.picked_items_assignment[i] = 1