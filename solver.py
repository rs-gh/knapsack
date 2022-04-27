#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from branch_and_bound import BranchAndBoundSolver
from naive_dp import NaiveDPSolver
from utils import log_metrics, debug_print
from logger import Logger


Item = namedtuple("Item", ['index', 'value', 'weight'])
logger = Logger()


@log_metrics
def solve(
    items,
    capacity,
    item_count,
    ks_index,
    search_strategy,
    estimation_method,
    order,
    epsilon,
    debug,
    logger
):
    if "dp" in search_strategy:
        solver = NaiveDPSolver(
            items, capacity, item_count, ks_index, order, debug
        )
    elif "bb" in search_strategy:
        solver = BranchAndBoundSolver(
            items, capacity, item_count, ks_index, search_strategy, estimation_method, order, epsilon, debug
        )
    solver.solve()
    return solver


def parse_input_and_solve(
    file_location,
    search_strategy="best_first_bb",
    estimation_method="feasible_greedy_estimate",
    order="descending_value_density",
    epsilon=0,
    debug=False
):
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    ks_index = file_location[file_location.index("ks_"):]
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # supply kwargs to log metrics
    return solve(
        items=items,
        capacity=capacity,
        item_count=item_count,
        ks_index=ks_index,
        search_strategy=search_strategy,
        estimation_method=estimation_method,
        order=order,
        epsilon=epsilon,
        debug=debug,
        logger=logger
    ), logger
