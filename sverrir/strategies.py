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


class OptimizedMovingAverageStrategy(Strategy):
    def __init__(self, window_size=50):
        self.window_size = window_size
        # Use a deque with a max length for an efficient sliding window
        self.prices = deque(maxlen=self.window_size)
        self.running_sum = 0.0

    def generate_signals(self, tick: MarketDataPoint) -> list:
        """
        Generates a signal by comparing the current price to the optimized moving average.
        """
        price = tick.price
        
        # Before the window is full, we can't generate a valid signal.
        # We also need to subtract the oldest price if the deque is already full.
        if len(self.prices) == self.window_size:
            # Subtract the oldest price (the one that's about to be pushed out)
            self.running_sum -= self.prices[0]
            
        # The deque's maxlen automatically handles removing the oldest element
        self.prices.append(price)
        self.running_sum += price
        
        # Wait until the window is full to generate signals
        if len(self.prices) < self.window_size:
            return []

        # Calculate the average in O(1) time
        mean_price = self.running_sum / len(self.prices)
        
        # Generate the signal
        if price > mean_price:
            return ['SELL'] # Mean-reversion: price is high, expect it to fall
        elif price < mean_price:
            return ['BUY']  # Mean-reversion: price is low, expect it to rise
        else:
            return []

