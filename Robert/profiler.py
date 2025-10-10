from memory_profiler import memory_usage
import timeit
from tqdm import tqdm
from data_loader import read_csv_to_immutable_list
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt



def profile_memory(func, func_args=(), func_kwargs=None, file_path=None):
    """The function runs another function that it is given (by name), 
    along with the arguments required for that function to execute. 
    It then returns both the results of the function and the maximum
    memory usage in MB at different intervals during its execution."""
    if func_kwargs is None:
        func_kwargs = {}
    mem_usage, result = memory_usage((func, func_args, func_kwargs), retval=True, interval=0.1)
    return max(mem_usage), result

def run_strategies_memory_check(strategy_name, price_list, max_memory = False):
    """The function returns memory usage at start, middle and end of the inputted strategy.
    It does not check the memory usage of the for loop itself that runs the strategy, 
    but rather checks just the mempry usage inside the strategy function. 
    
    If max_memory = True, then the function returns the maximum memory usage instead of list."""

    length = len(price_list)
    sample_memory = [0, length // 2, length - 1]
    strat = strategy_name()
    memory_list = []
    signals_list = [] 
    count = 0
    for tick in tqdm(price_list, desc="Running strategy"):
        if count in sample_memory:
            max_memory_usage, signal = profile_memory(strat.generate_signals, func_args=(tick,))
            memory_list.append(max_memory_usage)
            signals_list.append(signal)
        else:
            signal = strat.generate_signals(tick)
            signals_list.append(signal)
        count += 1
    if max_memory:
        return max(memory_list), signals_list
    else:
        return memory_list, signals_list

def run_data_loader_time_check(file_path):
    start_time = timeit.default_timer()
    price_history = read_csv_to_immutable_list(file_path)
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    return elapsed_time, price_history


def run_strategies_time_check(strategy_name, price_list):
    strat = strategy_name()
    signals_list = []
    start_time = timeit.default_timer()
    for tick in price_list:
        signal = strat.generate_signals(tick)
        signals_list.append(signal)
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    return elapsed_time, signals_list



def plot_profiling_results(price_history_dict, profiled_df):
    """
    Plot runtime and memory usage for multiple strategies and data loading.

    Parameters
    ----------
    profiled_df : dict
        Dictionary of the form:
        {strategy_name: {file_name: (max_mem, elapsed_time, signals)}}
    price_history_dict : dict
        Dictionary of the form:
        {file_name: (max_mem, elapsed_time, price_hist)}
    """
    
    # --- Extract data from profiled_df ---
    memory_data = {}
    time_data = {}
    for strat, files in profiled_df.items():
        memory_data[strat] = {f: vals[0] for f, vals in files.items()}  # max_mem
        time_data[strat] = {f: vals[1] for f, vals in files.items()}    # elapsed_time

    df_mem = pd.DataFrame(memory_data)
    df_time = pd.DataFrame(time_data)

    # --- Extract data from price_history_dict ---
    load_mem = {f: vals[0] for f, vals in price_history_dict.items()}
    load_time = {f: vals[1] for f, vals in price_history_dict.items()}

    df_load = pd.DataFrame({
        "Memory (MB)": load_mem,
        "Runtime (s)": load_time
    })

    # --- Create side-by-side plots ---
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharex=False)
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Plot 1: Runtime vs File Name (for strategies)
    for i, strat in enumerate(df_time.columns):
        axes[0].plot(df_time.index, df_time[strat], marker='o',
                     label=strat, color=colors[i % len(colors)])
    axes[0].set_xlabel("File name")
    axes[0].set_ylabel("Runtime (seconds)")
    axes[0].set_title("Runtime vs File Name (Strategies)")
    axes[0].legend()

    # Plot 2: Memory Usage vs File Name (for strategies)
    for i, strat in enumerate(df_mem.columns):
        axes[1].plot(df_mem.index, df_mem[strat], marker='o',
                     label=strat, color=colors[i % len(colors)])
    axes[1].set_xlabel("File name")
    axes[1].set_ylabel("Memory Usage (MB)")
    axes[1].set_title("Memory Usage vs File Name (Strategies)")
    axes[1].legend()

    # Plot 3: Data Loading (from price_history_dict)
    axes[2].plot(df_load.index, df_load["Runtime (s)"], marker='o',
                 color='tab:blue', label="Runtime (s)")
    axes[2].plot(df_load.index, df_load["Memory (MB)"], marker='o',
                 color='tab:orange', label="Memory (MB)")
    axes[2].set_xlabel("File name")
    axes[2].set_title("Data Loader Profiling")
    axes[2].legend()

    plt.tight_layout()
    output_path = "Robert/profiling_results.png"
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight", dpi=180)
    plt.close()
    print(f"Saved plot to {os.path.abspath(output_path)}")
