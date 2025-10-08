
from models import MarketDataPoint
from datetime import datetime
import csv

def load_market_data(file_path):
    data_points = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            timestamp = datetime.fromisoformat(row[0])
            symbol = row[1]
            price = float(row[2])
            data_points.append(MarketDataPoint(timestamp, symbol, price))
    return data_points, len(data_points)






