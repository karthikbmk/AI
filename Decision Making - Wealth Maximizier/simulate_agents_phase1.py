'''
Simulate agents - Phase 1
'''

import numpy as np
from agents import HalfProbAgent, RatioAgent, BuyAllAgent
from agent_kbangal2 import Agent_kbangal2
def simulate_agents(agents, value, num_products, alpha, beta, seed=None):
    
    agent_wealths = {}
    
    for agent in agents:
        agent_wealths[agent] = 0
    
    if seed is not None:
        np.random.seed(seed)
    
    for _ in range(num_products):
        # price is always lower than or equal to the value
        price = np.random.rand()*value
        
        # prob of being Excellent
        prob = np.random.beta(alpha, beta)
        
        # Excellent or not?
        excellent = prob > np.random.rand()
        
        for agent in agents:
            if agent.will_buy(value, price, prob):
                agent_wealths[agent] -= price
                if excellent:
                    agent_wealths[agent] += value
    
    return agent_wealths

if __name__ == '__main__':    
    
    value = 1000.
    
    num_products = 1000
    
    agents = []
    
    agents.append(HalfProbAgent("hp"))
    
    agents.append(RatioAgent("ratio_0.75", 0.75))
    agents.append(RatioAgent("ratio_0.50", 0.5))
    agents.append(RatioAgent("ratio_0.25", 0.25))
    agents.append(BuyAllAgent("buy_all"))
    agents.append(Agent_kbangal2("agent_kbangal2"))
    # add our own agent   
    #agents.append(Agent_<hawk_username>("agent_<hawk_username>"))

    # Change the seed so that it is your CWID,
    # excluding the initial 'A', of course.
    # seed needs to be an integer; not a string.
    seed = 20344597
    
    # Fair market; the ratio of Excellent to Trash products is 1:1
    agent_wealths = simulate_agents(agents, value, num_products, 1, 1, seed)
    
    print '-' * 50
    print 'FAIR MARKET'
    print '-' * 50
    for agent in agents:
        print "{}:\t\t${:,.2f}".format(agent, agent_wealths[agent])
    
    # Junk market; the ratio of Excellent to Trash products is 1:2
    agent_wealths = simulate_agents(agents, value, num_products, 1, 2, seed)
    
    print
    print '-' * 50
    print 'JUNK YARD'
    print '-' * 50
    for agent in agents:
        print "{}:\t\t${:,.2f}".format(agent, agent_wealths[agent])
    
    # Fancy market; the ratio of Excellent to Trash products is 2:1
    agent_wealths = simulate_agents(agents, value, num_products, 2, 1, seed)
    
    print
    print '-' * 50
    print 'FANCY MARKET'
    print '-' * 50
    for agent in agents:
        print "{}:\t\t${:,.2f}".format(agent, agent_wealths[agent])
