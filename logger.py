from collections import namedtuple
from itertools import product
import matplotlib.pyplot as plt
import numpy as np
import os


LogKey = namedtuple("LogKey", ["search_strategy", "estimation_method", "ks_index"])
LogEntry = namedtuple("LogEntry", ["pid", "time", "cache_size", "opt_value", "picked_items"])


class Logger:
    
    FILEPATH = "/mnt/c/Users/Shreyas/Desktop/Projects/discrete_optimization/knapsack/testing"
    
    def __init__(self, metadata=None):
        self.log = {}
        self.metadata = metadata
    
    
    def add_log(
        self,
        search_strategy,
        estimation_method,
        ks_index,
        time,
        cache_size,
        opt_value,
        picked_items
    ):
        self.log[LogKey(search_strategy, estimation_method, ks_index)] = LogEntry(os.getpid(), time, cache_size, opt_value, picked_items)
    
    
    @staticmethod
    def get_x_axis(k):
        try:
            return float(k[k.index("ks_")+3:].replace("_", "."))
        except ValueError:
            if k == "ks_lecture_dp_1":
                return -1
            else:
                return -2

            
    @staticmethod
    def plot_log(
        log,
        search_strategies,
        estimation_methods,
        log_scale_x_axis=False
    ):
        y_plot = ("time", "cache_size", "opt_value")
        plots = {
            (search_strategy, estimation_method): {
                Logger.get_x_axis(key.ks_index): log[key] for key in log.keys()
                if search_strategy == key.search_strategy and estimation_method == key.estimation_method
            }
            for search_strategy, estimation_method in product(search_strategies, estimation_methods) 
        }
        for y in y_plot:
            plt.figure()
            plt.title(y)
            for search_strategy, estimation_method in plots.keys():
                current_plot = plots[search_strategy, estimation_method]
                x_axis = sorted(current_plot.keys())
                y_axis = [getattr(current_plot[x], y) for x in x_axis]
                if log_scale_x_axis:
                    x_axis = np.log10(x_axis)
                plt.plot(x_axis, y_axis, marker="o", label=search_strategy+"/"+estimation_method)
            plt.legend()
            plt.savefig(Logger.FILEPATH + y + ".png")
            plt.show()