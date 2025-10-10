import data_loader
from data_loader import read_csv_to_immutable_list
from profiler import profile_memory
from models import Strategy
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy
from tqdm import tqdm



def run_strategies(strategy_name, price_list):
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
    return memory_list, signals_list
        


def main():
    file_path = "Robert/market_data.csv"
    max_memory_usage, price_list = profile_memory(read_csv_to_immutable_list, func_args=(file_path,))
    print("Successfully read the CSV file to MarketDataPoints.")
    print(f"Highest memory usage while reading CSV: {max_memory_usage:.2f} MB")

    #NMAT_memory_list, NMAT_signals_list = run_strategies_w_memory_check(NaiveMovingAverageStrategy, price_list)
    print('Running long strategy')
    #NMAT_memory_list, NMAT_signals_list = run_strategies_w_memory_check(NaiveMovingAverageStrategy, price_list)
    NMAT_memory_list, NMAT_signals_list = run_strategies(NaiveMovingAverageStrategy, price_list)
    print(NMAT_memory_list[:5], NMAT_signals_list[:5])
    print('Running þbetter strategy')
    #WMAS_memory_list, WMAS_signals_list = run_strategies_w_memory_check(WindowedMovingAverageStrategy, price_list)
    WMAS_memory_list, WMAS_signals_list = run_strategies(WindowedMovingAverageStrategy, price_list)
    print(WMAS_memory_list[:5], WMAS_signals_list[:5])


if __name__ == "__main__":
    main()

