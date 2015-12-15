'''
The agent base class as well as the baseline agents.
'''

from abc import abstractmethod


class Agent(object):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Agent_" + self.name

    @abstractmethod
    def will_buy(self, value, price, prob):
        """Given a value, price, and prob of Excellence,
        return True if you want to buy it; False otherwise.
        Override this method."""

class KarthikAgent(Agent):
    #higher the price, higher the risk of losing..Hence taking risks only for lower prices.
    
    def will_buy(self, value, price, prob):
        if prob > 0.5:
            return True
        elif prob > 0.4 and price < 150: 
            return True
 

class HalfProbAgent(Agent):
    """Buys if the prob > 0.5 no matter what the value or price is"""
    
    def will_buy(self, value, price, prob):
        return (prob > 0.5)

class RatioAgent(Agent):
    """Buys if the ratio of the price to value is below a specified threshold"""
    
    def __init__(self, name, max_p_v_ratio):
        super(RatioAgent, self).__init__(name)
        self.max_p_v_ratio = max_p_v_ratio
    
    def will_buy(self, value, price, prob):
        return (price/value <= self.max_p_v_ratio)

class BuyAllAgent(Agent):
    """Simply buys all products"""
    
    def will_buy(self, value, price, prob):
        return True   

