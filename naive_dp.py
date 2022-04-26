from knapsack_solver import KnapsackSolver
from utils import debug_print
from bound_estimate import BoundEstimate


class NaiveDPSolver(KnapsackSolver):
    def __init__(self, items, capacity, item_count, ks_index, order=None, debug=False):
        super().__init__(items, capacity, item_count, ks_index, order, debug)


    def O(self, k, j):
        item = self.items[j-1]
        debug_print(k, "\t", j, debug=self.debug)
        debug_print("item weight: {}".format(item.weight), debug=self.debug)
        try:
            return self.cache[(k, j)]
        except KeyError:
            if j == 0:
                self.cache[(k, j)] = 0
            elif item.weight > k:
                self.cache[(k, j)] = self.O(k, j-1)
            else:
                self.cache[(k, j)] = max(
                    self.O(k, j-1),
                    item.value + self.O(k-item.weight, j-1)
                )
            return self.cache[(k, j)]


    def backtrack(self, k, j):
        if j == 0:
            return
        item = self.items[j-1]
        if self.cache[(k, j)] != self.cache[(k, j-1)]:
            self.picked_items.append(item.index)
            self.backtrack(k-item.weight, j-1)
        else:
            self.backtrack(k, j-1)


    def solve(self):
        self.value = self.O(self.capacity, self.item_count)
        self.backtrack(self.capacity, self.item_count)
        self.get_picked_items_assignment()
