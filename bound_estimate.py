from utils import debug_print


class BoundEstimate:
    def __init__(self):
        pass


    @staticmethod
    def is_estimate_within_epsilon_bound_of_or_gt_current_max_estimate(estimate, current_max, epsilon=0):
        if estimate >= current_max:
            return True
        return (current_max - estimate) <= (epsilon * current_max)


    @staticmethod
    def get_optimistic_assignment(assignment, item_count):
        return assignment + [1 for _ in range(item_count - len(assignment))]


    @staticmethod
    def greedy_estimate(items, capacity, item_count, assignment, estimate=None, linear_relaxation=True):
        assignment = BoundEstimate.get_optimistic_assignment(assignment, item_count)
        debug_print("optimistic assignment is: {}".format(assignment), debug=False)
        if estimate is None:
            estimate = 0
        for i in range(item_count):
            if capacity <= 0:
                break
            if assignment[i] == 0:
                continue
            if linear_relaxation:
                capacity_ratio = min(capacity * 1.0/items[i].weight, 1.0)
                estimate += items[i].value * capacity_ratio
                capacity -= items[i].weight * capacity_ratio
            else:
                if items[i].weight > capacity:
                    continue
                else:
                    estimate += items[i].value
                    capacity -= items[i].weight
        return estimate


    @staticmethod
    def unconstrained_estimate(items, capacity, item_count, assignment, estimate=None):
        assignment = BoundEstimate.get_optimistic_assignment(assignment, item_count)
        if estimate is None:
            estimate = 0
        for i in range(item_count):
            if assignment[i] == 0:
                continue
            else:
                estimate += items[i].value
        return estimate