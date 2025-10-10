import data_loader
from data_loader import read_csv_to_immutable_list
from profiler import profile_memory, run_strategies_memory_check, run_strategies_time_check, run_data_loader_time_check, plot_profiling_results
from models import Strategy
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy
from tqdm import tqdm
import timeit
import pandas as pd

def main():
    strategies = [NaiveMovingAverageStrategy, WindowedMovingAverageStrategy]
    file_paths = ["Robert/market_data_1k.csv", "Robert/market_data_10k.csv", "Robert/market_data_100k.csv"]
    
    # Check time and memory usage to load CSV to MarketDataPoints
    price_history_dict = {}
    for file_path in file_paths:
        max_memory_usage, price_hist = profile_memory(read_csv_to_immutable_list, func_args=(file_path,))
        elapsed_time, price_hist = run_data_loader_time_check(file_path)
        price_history_dict[file_path] = (max_memory_usage, elapsed_time, price_hist)
        
    print("Successfully read the CSV files to MarketDataPoints, and profiled the memory usage and time elapsed for each file.")
    #print(f"Highest memory usage while reading CSV: {max_memory_usage:.2f} MB")
    
    profiled_df = { 
    (s.__name__ if hasattr(s, "__name__") else str(s)): {} 
    for s in strategies
    }

    for strat in strategies:
        price_hist = price_history_dict[file_path][2]
        strat_name = strat.__name__ if hasattr(strat, "__name__") else str(strat)
        for file_path in file_paths:
            price_hist = price_history_dict[file_path][2]
            max_mem, signals = run_strategies_memory_check(strat, price_hist, max_memory = True)
            elapsed_time, signals = run_strategies_time_check(strat, price_hist)
            profiled_df[strat_name][file_path] = (max_mem, elapsed_time, signals)
    
    plot_profiling_results(price_history_dict, profiled_df)

if __name__ == "__main__":
    main()

