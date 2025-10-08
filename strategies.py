from models import MarketDataPoint
from abc import ABC, abstractmethod
from collections import deque

class Strategy(ABC):

    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

class NaiveMovingAverageStrategy(Strategy):
    def __init__(self):
        self.prices = []
    
    def generate_signals(self, tick):
        price = tick.price
        if len(self.prices) == 0:
            self.prices.append(price)
            return []
        else:
            mean_price = sum(self.prices) / len(self.prices)
            if price < mean_price:
                signal = ['BUY']
            elif price > mean_price:
                signal = ['SELL']
            else:
                signal = []
            self.prices.append(price)
        return signal
    

class WindowedMovingAverageStrategy(Strategy):
    def __init__(self, window = 20):
        self.window = window
        self.prices = deque()
        self.running_sum = 0
    
    def generate_signals(self, tick):
        price = tick.price
        if len(self.prices) < self.window:
            self.prices.append(price)
            self.running_sum += price
            return []
        else:
            mean_price = self.running_sum / len(self.prices)
            if price < mean_price:
                signal = ['BUY']
            elif price > mean_price:
                signal = ['SELL']
            else:
                signal = []
            removed_price = self.prices.popleft()
            self.running_sum -= removed_price
            self.prices.append(price)
            self.running_sum += price
            return signal




