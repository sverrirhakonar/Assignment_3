import timeit
import cProfile
from data_loader import load_market_data
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy
from models import MarketDataPoint

TICK_SIZES = [1_000, 10_000, 100_000]
def run_simulation(strategy, data):
    for tick in data:
        strategy.generate_signals(tick)

all_data = load_market_data('market_data.csv')

# Create a slice of data for this specific experiment


setup_code = """
from strategies import NaiveMovingAverageStrategy
strategy = NaiveMovingAverageStrategy()
"""
stmt_code = "run_simulation(strategy, data_1k)"
num_runs = 10

for n in TICK_SIZES:
    # Run the timer!
    print('Tick_size = ', n)
    data = all_data[:n]
    total_time = timeit.timeit(
        stmt=stmt_code,
        setup=setup_code,
        number=num_runs,
        globals={
            "run_simulation": run_simulation,
            "data_1k": data
        }
    )

    # --- 3. RESULTS ---

    avg_time_per_run = total_time / num_runs

    print(f"Completed {num_runs} runs in {total_time:.6f} seconds.")
    print(f"Average time per run: {avg_time_per_run:.6f} seconds.")


