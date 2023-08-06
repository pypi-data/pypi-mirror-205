import time

def wait(wait_time, current_time=time.perf_counter):
    """Suspends the current thread for a specified amount of time.

    Parameters
    ----------
    wait_time: float
        Wait time in seconds to suspend the current thread.
    current_time: float
        The current time in seconds. Default is time.perf_counter(), which is the result from a high resolution clock
    """
    now = current_time()
    end = now + wait_time
    while now < end:
        now = current_time()