from time import time
from functools import wraps


def debug_print(*args, debug=False):
    if debug:
        print(*args)


def log_metrics(f):
    @wraps(f)
    def logged_run(*args, **kwargs):
        start = time()
        y = f(*args, **kwargs)
        end = time()
        delta = end - start
        kwargs["logger"].add_log(
            kwargs["search_strategy"], kwargs["estimation_method"], kwargs["ks_index"], delta, len(y.cache), y.value, y.picked_items)
        return y
    return logged_run