from models import MarketDataPoint
from datetime import datetime
import csv


# Space Complexity: O(N) where N is the number of data rows in the csv file.
# The function stores every parsed MarketDataPoint object in the data_points list,
# so memory usage grows linearly with the number of rows.
def load_market_data(file_path):
    '''Function that loads the market data to a list of MarketDataPoints '''
    data_points = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            timestamp = datetime.fromisoformat(row[0])
            symbol = row[1]
            price = float(row[2])
            data_points.append(MarketDataPoint(timestamp, symbol, price))
    return data_points



