import numpy as np
from functools import partial
from knapsack_solver import KnapsackSolver
from utils import debug_print
from bound_estimate import BoundEstimate
from heap import Heap


class BranchAndBoundSolver(KnapsackSolver):
    def __init__(
        self, items, capacity, item_count, ks_index,
        search_strategy, estimation_method, order, epsilon,
        debug=False
    ):
        if estimation_method == "linear_relaxation":
            order = "descending_value_density"
            self.get_estimate = partial(BoundEstimate.greedy_estimate, linear_relaxation=True)
        elif estimation_method == "feasible_greedy_estimate":
            self.get_estimate = partial(BoundEstimate.greedy_estimate, linear_relaxation=False)
        elif estimation_method == "unconstrained_estimate":
            self.get_estimate = BoundEstimate.unconstrained_estimate
        if search_strategy == "depth_first_bb":
            self.search_strategy = self.depth_first_search
        elif search_strategy == "best_first_bb":
            self.search_strategy = self.best_first_search
        elif search_strategy == "lds_bb":
            self.search_strategy = self.least_discrepancy_search
        super().__init__(items, capacity, item_count, ks_index, order, debug, epsilon)
        self.running_max_estimate = 0
        self.running_max_assignment = None
        self.running_max_assignment_depth = 0


    def is_feasible_assignment(self, assignment, assignment_depth):
        weights = [self.items[i].weight for i in range(assignment_depth)]
        assignment_weight = np.inner(weights, assignment)
        return assignment_weight <= self.capacity


    def depth_first_search(self):
        stack = []
        stack.append([0])
        stack.append([1])

        while True:
            try:
                assignment = stack.pop()
                assignment_depth = len(assignment)
                debug_print("dfs: current assignment is: {}".format(assignment), debug=self.debug)
                if self.is_feasible_assignment(assignment, assignment_depth):
                    estimate = self.get_estimate(self.items, self.capacity,self.item_count, assignment)
                    debug_print("dfs: optimistic estimate is: {}".format(estimate), debug=self.debug)
                    if assignment_depth <= self.running_max_assignment_depth and not BoundEstimate.is_estimate_within_epsilon_bound_of_or_gt_current_max_estimate(estimate, self.running_max_estimate, self.epsilon):
                        debug_print("discarding assignment with estimate {}, while running_max_assignment is {} with estimate {}".format(assignment, estimate, self.running_max_assignment, self.running_max_estimate), debug=self.debug)
                        continue
                    else:
                        if assignment_depth >= self.running_max_assignment_depth:
                            self.running_max_estimate = estimate
                            self.running_max_assignment = assignment
                            self.running_max_assignment_depth = assignment_depth
                        if assignment_depth < self.item_count:
                            stack.append(assignment + [0])
                            stack.append(assignment + [1])
                            debug_print("dfs: after adding nodes, stack is: {}".format(stack), debug=self.debug)
                else:
                    debug_print("assignment is infeasible", debug=self.debug)
                        
            except IndexError:
                break


    def best_first_search(self):
        heap = Heap()
        for assignment in [[0], [1]]:
            assignment_depth = len(assignment)
            if self.is_feasible_assignment(assignment, assignment_depth):
                heap.add_to_heap(
                    HeapNode(assignment, assignment_depth, self.get_estimate(self.items, self.capacity, self.item_count, assignment))
                )
        while not heap.is_empty():
            node = heap.get_heap_max()
            assignment = node.assignment
            assignment_depth = node.assignment_depth
            estimate = node.value
            debug_print("bfs: current assignment is: {} of depth {}".format(assignment, assignment_depth), debug=self.debug)

            if assignment_depth <= self.running_max_assignment_depth and not BoundEstimate.is_estimate_within_epsilon_bound_of_or_gt_current_max_estimate(estimate, self.running_max_estimate, self.epsilon):
                debug_print("discarding assignment with estimate {}, while running_max_assignment is {} with estimate {}".format(assignment, estimate, self.running_max_assignment, self.running_max_estimate), debug=self.debug)
                continue
            else:
                if assignment_depth > self.running_max_assignment_depth or (assignment_depth == self.running_max_assignment_depth and estimate > self.running_max_estimate):
                    self.running_max_estimate = estimate
                    self.running_max_assignment = assignment
                    self.running_max_assignment_depth = assignment_depth
                if assignment_depth < self.item_count:
                    for child in [[0], [1]]:
                        new_assignment = assignment + child
                        new_assignment_depth = assignment_depth + 1
                        debug_print("bfs: new assignment is: {}".format(new_assignment), debug=self.debug)
                        if self.is_feasible_assignment(new_assignment, new_assignment_depth):
                            heap.add_to_heap(
                                HeapNode(new_assignment, new_assignment_depth, self.get_estimate(self.items, self.capacity, self.item_count, new_assignment))
                            )
                        else:
                            debug_print("bfs: new assignment is infeasible", debug=self.debug)
                    debug_print("bfs: after adding nodes, heap is: {}".format(heap.heap), debug=self.debug)


    def _lds_probe(self, assignment, assignment_depth, discrepancies):
        debug_print("lds: assignment is: {}".format(assignment), debug=self.debug)
        if not self.is_feasible_assignment(assignment, assignment_depth):
            debug_print("lds: assignment is infeasible", debug=self.debug)
            self.cache[tuple(assignment)] = False
            return

        try:
            if self.cache[tuple(assignment)] == False:
                debug_print("lds: assignment not explored", debug=self.debug)
                return
        except KeyError:
            self.cache[tuple(assignment)] = self.get_estimate(self.items, self.capacity, self.item_count, assignment)

        assignment_estimate = self.cache[tuple(assignment)]
        if assignment_depth < self.running_max_assignment_depth and not BoundEstimate.is_estimate_within_epsilon_bound_of_or_gt_current_max_estimate(assignment_estimate, self.running_max_estimate, self.epsilon):
            # can't eliminate equal depth nodes because we repeatedly traverse the same nodes
            debug_print(
                "lds: discarding assignment, assignment_estimate of depth {} is {}, while running max is {} with depth {}"
                .format(assignment_estimate, assignment_depth, self.running_max_estimate, self.running_max_assignment_depth),
                debug=self.debug
            )
            self.cache[tuple(assignment)] = False
            return
        elif assignment_depth > self.running_max_assignment_depth or (assignment_depth == self.running_max_assignment_depth and assignment_estimate >= self.running_max_estimate):
            debug_print(
                "lds: updating max estimates, assignment_estimate is {} at depth {}, while running max is {} at depth {}"
                .format(assignment_estimate, assignment_depth, self.running_max_estimate, self.running_max_assignment_depth),
                debug=self.debug
            )
            self.running_max_estimate = assignment_estimate
            self.running_max_assignment = assignment
            self.running_max_assignment_depth = assignment_depth
        if assignment_depth+1 <= self.item_count:
            self._lds_probe(assignment+[1], assignment_depth+1, discrepancies)
            if discrepancies > 0:
                self._lds_probe(assignment+[0], assignment_depth+1, discrepancies-1)


    def least_discrepancy_search(self):
        for wave_number in range(self.item_count+1):
            debug_print("lds: wave_number is {}".format(wave_number), debug=self.debug)
            self._lds_probe([1], 1, wave_number)
            if wave_number > 0:
                self._lds_probe([0], 1, wave_number-1)
        

    def solve(self):
        self.search_strategy()    
        self.value = self.running_max_estimate
        self.picked_items = [self.items[i].index for i in range(self.item_count) if self.running_max_assignment[i] == 1]
        debug_print("final assignment: {}".format(self.running_max_assignment), debug=self.debug)
        debug_print("picked items: {}".format(self.picked_items), debug=self.debug)
        self.get_picked_items_assignment()