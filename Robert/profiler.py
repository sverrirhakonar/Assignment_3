from memory_profiler import memory_usage

# def profile_memory(func, *args, **kwargs):
    
#     """The function runs another function that it is given (by name), 
#     along with the arguments required for that function to execute. 
#     It then returns both the results of the function and the maximum
#     memory usage in MB at different intervals during its execution."""

#     mem_usage, result = memory_usage((func, args, kwargs), retval=True, interval=0.001)
#     return max(mem_usage), result


def profile_memory(func, func_args=(), func_kwargs=None, file_path=None):
    if func_kwargs is None:
        func_kwargs = {}
    mem_usage, result = memory_usage((func, func_args, func_kwargs), retval=True, interval=0.001)
    return max(mem_usage), result