'''
Simulate agents - Phase 2
'''

import numpy as np

from agents import Agent_single_sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC

# import your own agent. Change mbilgic to your own hawk id
from agent_kbangal2 import Agent_kbangal2

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
    data_groups = ["dataset1", "dataset2", "dataset3"]
    for data_group in data_groups:
        
        train_file = data_path + data_group +  "_train.csv"
        val_file = data_path + data_group +  "_val.csv"
        test_file = data_path + data_group +  "_test.csv"
        
        train_data=np.loadtxt(train_file, dtype=str, delimiter=',', skiprows=1)
        X_train=train_data[:, 0:-1]=='T'
        y_train=train_data[:, -1]

        val_data=np.loadtxt(val_file, dtype=str, delimiter=',', skiprows=1)
        X_val=val_data[:, 0:-1]=='T'
        y_val=val_data[:, -1]

        test_data=np.loadtxt(test_file, dtype=str, delimiter=',', skiprows=1)
        X_test=test_data[:, 0:-1]=='T'
        y_test=test_data[:, -1]
        
        agents = []
        
        agents.append(Agent_single_sklearn("bnb", BernoulliNB()))
        # Add two more Agent_single_sklearn agents
        # One that uses LogisticRegression using default constructor
        agents.append(Agent_single_sklearn("lr", LogisticRegression()))
        # One that uses SVC with polynomial kernel degree of 4 and
        # probability estimates are turned on
        agents.append(Agent_single_sklearn("svc",  SVC(degree=4,probability=True,random_state=0)))
        # Add your own agent; change mbilgic to your own hawk id
        agents.append(Agent_kbangal2("kbangal2"))
        
        # Train the agents
        for agent in agents:
            agent.train(X_train, y_train, X_val, y_val)
        
        # Simulate the agents on test
        value = 1000
        agent_wealths = simulate_agents(agents, value, X_test, y_test)
        
        print "-" * 50
        print "SIMULATION RESULTS ON %s" %(data_group)
        print "-" * 50

        print "\nWealth (the larger the better)\n"
        for agent in agents:
            print "{}:\t\t${:,.2f}".format(agent, agent_wealths[agent])

        # Log-loss
        print "\nLog-loss (the smaller the better)\n"
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

        # 0/1 Loss
        print "\n0/1 Loss (the smaller the better)\n"
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
