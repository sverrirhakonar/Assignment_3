import csv
from models import MarketDataPoint
from datetime import datetime

# @dataclass(frozen=True)
# class MarketDataPoint:
#     timestamp: datetime
#     symbol: str
#     price: float

def read_csv_to_immutable_list(csv_file_name):

    """The function takes a CSV file path and returns it as a list of MarketDataPoints"""

    with open(csv_file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        price_history = []
        for point in reader:
            market_data_point = MarketDataPoint(
                timestamp = datetime.fromisoformat(point["timestamp"]), 
                symbol = point['symbol'], 
                price = float(point['price']))
            price_history.append(market_data_point)
    return price_history
