from models import MarketDataPoint
from abc import ABC, abstractmethod
from collections import deque

class Strategy(ABC):

    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

# Space Complexity: O(n)
# The list self.prices grows indefinitely and linearly with terms of input size
class NaiveMovingAverageStrategy(Strategy):
    def __init__(self):
        self.prices = []
    
    # Time Complexity: O(n)
    # The sum function for calculating the mean price iterates,
    # over the entire list, and calculates the sum.
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
    

# Space Complexity: O(k), where k is the window size
# Self.prices implements a deque that inserts and removes element, keeping the space fixed by the window size.
class WindowedMovingAverageStrategy(Strategy):
    def __init__(self, window = 20):
        self.window = window
        self.prices = deque()
        self.running_sum = 0
    
    # Time Complexity: O(1)
    # The running sum keeps the sum, it updates by subtracting the removed value and adds 
    # the most recent price to the sum, both at a constant O(1) time complexity.

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




