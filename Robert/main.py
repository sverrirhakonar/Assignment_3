import data_loader
from data_loader import read_csv_to_immutable_list
from profiler import profile_memory

def main():
    mem_usage, result = profile_memory(read_csv_to_immutable_list, "Robert/market_data.csv")
    #print(result)
    print(mem_usage)
    max_memory = max(mem_usage)
    print(max_memory)

if __name__ == "__main__":
    main()

