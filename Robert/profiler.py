from memory_profiler import memory_usage

def profile_memory(func, *args, **kwargs):
    
    """The function runs another function that it is given (by name), 
    along with the arguments required for that function to execute. 
    It then returns both the results of the function and the memory 
    usage at different intervals during its execution."""

    mem_usage, result = memory_usage((func, args, kwargs), retval=True, interval=0.001)
    return mem_usage, result