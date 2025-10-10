from models import Strategy
from collections import deque

class NaiveMovingAverageStrategy(Strategy):
    def __init__(self):
        self.prices = []
    
    # Theo time complexity: O(n), calculates the sum each time with +1 longer list each time.
    # Theo space complexity: O(n), the list of prices gets larger and larger with each step, until n steps have been performed.
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
    
    # Theo time complexity: O(1), just modifies the sum each time by adding and replacing the oldest value. 
    # Theo space complexity: O(window size) ~ O(1), keeps the length of the rolling sum, so it is techically O(window size).
    def generate_signals(self, tick):
        price = tick.price
        length = len(self.prices)
        if length < self.window:
            self.prices.append(price)
            self.running_sum += price
            return []
        else:
            mean_price = self.running_sum / length
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