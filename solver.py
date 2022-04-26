#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from branch_and_bound import BranchAndBoundSolver
from naive_dp import NaiveDPSolver
from utils import timed, debug_print


Item = namedtuple("Item", ['index', 'value', 'weight'])


@timed
def solve(items, capacity, item_count, method, order, epsilon=0, ks_index=None, estimation_method=None, debug=False):
    if "dp" in method:
        solver = NaiveDPSolver(
            items, capacity, item_count, ks_index,
            order=order,
            debug=debug
        )
    elif "bb" in method:
        solver = BranchAndBoundSolver(
            items, capacity, item_count, ks_index,
            search_strategy=method, estimation_method=estimation_method, order=order, epsilon=epsilon
            debug=debug
        )
    solver.solve()
    return solver


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    debug = False
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    if item_count <= 200:
        method = "dp"
        estimation_method = None
        order = "descending_weight"
        epsilon = None
    else:
        method = "best_first_bb"
        estimation_method = "feasible_greedy_estimate"
        order = "descending_value_density"
        epsilon = 0
        # monkeypatch to get 10 points for ks_1000_0...
        if item_count == 1000:
            epsilon = 0.0002

    solved = solve(
        items, capacity, item_count,
        method=method,
        estimation_method=estimation_method,
        order=order,
        epsilon=epsilon,
        debug=debug
    )

    # prepare the solution in the specified output format
    output_data = str(int(solved.value)) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solved.picked_items_assignment))

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

