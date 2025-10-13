import timeit
import cProfile
from data_loader import load_market_data
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, OptimizedMovingAverageStrategy
from models import MarketDataPoint
from memory_profiler import memory_usage
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def run_simulation(strategy, data):
    for tick in data:
        strategy.generate_signals(tick)

def test_average_runtime(strategy_class, tick_size, num_runs, all_data):
    data_slice = all_data[:tick_size]
    total_time = timeit.timeit(
        # Use a lambda to create a fresh strategy instance for each run
        lambda: run_simulation(strategy_class(), data_slice),
        number=num_runs
    )
    return total_time / num_runs

def test_peak_memory(strategy_class, data_slice):
    # Create one instance to run the memory test on
    strategy_instance = strategy_class()
    # memory_usage returns a list of memory snapshots over time
    mem_profile = memory_usage(
        (run_simulation, (strategy_instance, data_slice)),
        interval=0.01  # Check memory usage every 10ms
    )
    return max(mem_profile)

def main():
    all_data = load_market_data('market_data.csv')
    STRATEGIES_TO_TEST = [NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, OptimizedMovingAverageStrategy]
    TICK_SIZES = [10000, 20000, 40000, 60000, 80000, 100000]
    NUMBER_OF_RUNS = 10

    results = []
    i = 0
    for strategy_class in STRATEGIES_TO_TEST:
            for size in TICK_SIZES:
                data_slice = all_data[:size]

                avg_runtime = test_average_runtime(strategy_class, size, NUMBER_OF_RUNS, all_data)
                max_memory_usage = test_peak_memory(strategy_class, data_slice)
                results.append({"Strategy": strategy_class.__name__, "Ticks": size, "Avg Time":avg_runtime, "Peak Memory (MB)": max_memory_usage})
                i += 1
                print(f'run nr: {i}')

    results = pd.DataFrame(results)
    results['factor'] = results['Avg Time'] / results['Avg Time'].shift(1)
    print(results)

    print("Generating plots...")

    # Create a 1x2 grid for the plots
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Strategy Performance Analysis', fontsize=16)

    # Plot 1: Runtime vs. Ticks
    sns.lineplot(ax=axes[0], data=results, x='Ticks', y='Avg Time', hue='Strategy')
    axes[0].set_title('Runtime Scaling Analysis')
    axes[0].set_xlabel('Number of Ticks')
    axes[0].set_ylabel('Average Execution Time (s)')

    # Plot 2: Memory vs. Ticks
    sns.lineplot(ax=axes[1], data=results, x='Ticks', y='Peak Memory (MB)', hue='Strategy')
    axes[1].set_title('Memory Usage Scaling')
    axes[1].set_xlabel('Number of Ticks')
    axes[1].set_ylabel('Peak Memory Usage (MiB)')

    # Display the plots
    plt.tight_layout()
    plt.show()

    # You can also save the figure for your report
    fig.savefig("performance_analysis_plots.png")


if __name__ == '__main__':
    main()