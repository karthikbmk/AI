from agents import Agent

class Agent_kbangal2(Agent):
    #higher the price, higher the risk of losing..Hence taking risks only for lower prices.
    
    def will_buy(self, value, price, prob):
        if prob > 0.5:
            return True
        elif prob > 0.4 and price < 150: 
            return True
