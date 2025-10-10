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
    file_path_name_dict = {"Robert/market_data_1k.csv" : "1k", "Robert/market_data_10k.csv": "10k", "Robert/market_data_100k.csv": "100k"}
    # Check time and memory usage to load CSV to MarketDataPoints
    price_history_dict = {}
    for file_path in file_paths:
        max_memory_usage, price_hist = profile_memory(read_csv_to_immutable_list, func_args=(file_path,))
        elapsed_time, price_hist = run_data_loader_time_check(file_path)
        price_history_dict[file_path] = (max_memory_usage, elapsed_time, price_hist)
        
    print("Successfully read the CSV files to MarketDataPoints, and profiled the memory usage and time elapsed for each file.")
    
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
            file_label = file_path_name_dict[file_path]
            profiled_df[strat_name][file_label] = (max_mem, elapsed_time, signals)
    
    plot_profiling_results(price_history_dict, profiled_df)
    print("Successfully ran memory and time checks for each strategy and plotted the performance.")
    return price_history_dict, profiled_df


if __name__ == "__main__":
    # First run: compute metrics and generate plots
    price_history_dict, profiled_df = main()

    # Build tables for the markdown
    import pandas as pd
    from io import StringIO

    # Table for loader metrics
    loader_rows = []
    for fp, (max_mem_mb, load_time_s, _hist) in price_history_dict.items():
        loader_rows.append({
            "file": fp,
            "load_time_s": load_time_s,
            "peak_mem_mb": max_mem_mb,
        })
    loader_df = pd.DataFrame(loader_rows)

    # Table for strategy metrics
    strat_rows = []
    for strat_name, per_file in profiled_df.items():
        for fp, (max_mem_mb, run_time_s, signals) in per_file.items():
            # signals might not be a sequence depending on your implementation
            sig_count = len(signals) if hasattr(signals, "__len__") else None
            strat_rows.append({
                "strategy": strat_name,
                "file": fp,
                "run_time_s": run_time_s,
                "peak_mem_mb": max_mem_mb,
                "signals_count": sig_count,
            })
    strategies_df = pd.DataFrame(strat_rows)

    # Convert DataFrames to markdown text
    def df_to_md(df):
        try:
            return df.to_markdown(index=False)
        except Exception:
            return df.to_string(index=False)

    loader_md = df_to_md(loader_df)
    strategies_md = df_to_md(strategies_df)

    # Write the main sections of the report (overwrites file each run)
    report_path = "Robert/complexity_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Complexity Report\n\n")
        f.write("## Tables of runtime and memory metrics\n\n")
        f.write("### Data loading\n\n")
        f.write(loader_md)
        f.write("\n\n### Strategies\n\n")
        f.write(strategies_md)
        f.write("\n\n## Plots of scaling behavior\n\n")
        # Add your plot references here; see section 3 below for details
        # Examples:
        f.write("![Time and memory profile](Robert/profiling_results.png)\n\n")


        f.write("## Narrative comparing strategies and optimization impact\n\n")
        f.write("Add your analysis here. Compare throughput, latency, and memory across dataset sizes. Note any optimizations and their impact.\n\n")

    # Second run: cProfile the workload and append the stats to the report
    import cProfile, pstats, io

    pr = cProfile.Profile()

    # If you want to profile exactly the same workload as main:
    pr.enable()
    main()  # runs the whole pipeline again under the profiler
    pr.disable()

    # Capture top entries by cumulative time
    s = io.StringIO()
    pstats.Stats(pr, stream=s).sort_stats("cumtime").print_stats(50)
    cprofile_text = s.getvalue()

    # Append cProfile output to the markdown
    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n## Additional profiling: cProfile\n\n")
        f.write("```\n")
        f.write(cprofile_text)
        f.write("\n```\n")
    

