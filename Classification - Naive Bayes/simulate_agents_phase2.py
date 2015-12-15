'''
Simulate agents - Phase 2
'''

import numpy as np

from agents import FixedProbAgent
# import your own agent. Change mbilgic to your own hawk id
#from agent_mbilgic import Agent_mbilgic

def simulate_agents(agents, value, X, y, price_trials = 10):
    
    agent_wealths = {}
    
    for agent in agents:
        agent_wealths[agent] = 0
    
    num_products = X.shape[0]
    
    for p in range(num_products):        
        
        # Excellent or not?
        excellent = (y[p] == 'Excellent')
        
        for agent in agents:
            prob = agent.predict_prob_of_excellent(X[p])
            # try a range of prices            
            for pt in range(price_trials):                            
                price = ((2*pt+1)*value)/(2*price_trials)                                
                if agent.will_buy(value, price, prob):
                    agent_wealths[agent] -= price
                    if excellent:
                        agent_wealths[agent] += value
    return agent_wealths

if __name__ == '__main__':

    # You might need to change this depending on where the data is located
    data_path = "./"
    data_groups = ["dataset1", "dataset2", "dataset3", "dataset4"]
    for data_group in data_groups:
        
        train_file = data_path + data_group +  "_train.csv"
        test_file = data_path + data_group +  "_test.csv"
        
        train_data=np.loadtxt(train_file, dtype=str, delimiter=',', skiprows=1)
        X_train=train_data[:, 0:-1]=='T'
        y_train=train_data[:, -1]

        test_data=np.loadtxt(test_file, dtype=str, delimiter=',', skiprows=1)
        X_test=test_data[:, 0:-1]=='T'
        y_test=test_data[:, -1]

        
        agents = []
        
        agents.append(FixedProbAgent("fixed_prob_0.00", 0.))
        agents.append(FixedProbAgent("fixed_prob_0.25", 0.25))
        agents.append(FixedProbAgent("fixed_prob_0.50", 0.50))
        agents.append(FixedProbAgent("fixed_prob_0.75", 0.75))
        agents.append(FixedProbAgent("fixed_prob_1.00", 1.))
        # add our own agent; change mbilgic to your own hawk id
        #agents.append(Agent_mbilgic("mbilgic"))
        
        # Train the agents
        for agent in agents:
            agent.train(X_train, y_train)
        
        # Simulate the agents
        value = 1000
        agent_wealths = simulate_agents(agents, value, X_test, y_test)
        
        print "-" * 50
        print "SIMULATION RESULTS ON %s" %(data_group)
        print "-" * 50

        print "\nWealth (the larger the better)\n"
        for agent in agents:
            print "{}:\t\t${:,.2f}".format(agent, agent_wealths[agent])

        # Log loss
        print "\nPrediction Log-loss (the smaller the better)\n"
        epsilon = 1e-10
        for agent in agents:
            ll = 0
            num_products = X_test.shape[0]
            for p in range(num_products):
                prob = agent.predict_prob_of_excellent(X_test[p])
                if y_test[p] == 'Excellent':
                    ll += -(np.log(prob+epsilon))
                else:
                    ll += -(np.log(1-prob+epsilon))
            print "{}:\t\t{:,.2f}".format(agent, ll)

        # Error
        print "\nPrediction Error (the smaller the better)\n"
        for agent in agents:
            error = 0
            num_products = X_test.shape[0]
            for p in range(num_products):
                prob = agent.predict_prob_of_excellent(X_test[p])
                if y_test[p] == 'Excellent':
                    if prob < 0.5:
                        error += 1
                else:
                    if prob >= 0.5:
                        error += 1
            print "{}:\t\t{:,d}".format(agent, error)
