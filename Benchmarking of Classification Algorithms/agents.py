'''
The agent base class as well as a baseline agent.
'''

from abc import abstractmethod


class Agent(object):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Agent_" + self.name
    
    def will_buy(self, value, price, prob):
        """Given a value, price, and prob of Excellence,
        return True if you want to buy it; False otherwise.
        The rational agent.
        Do NOT change or override this."""
        return value*prob > price

    def train(self, X_train, y_train, X_val, y_val):
        """First, choose the best classifier that when trained
        on <X_train, y_train> performs the best on <X_val, y_val>.
        Then, train that classifier on X_train, y_train.
        Do NOT change or override this method.
        """
        self.clf = self.choose_the_best_classifier(X_train, y_train, X_val, y_val)

        # Train the classifier
        self.clf.fit(X_train, y_train)

        # Find the index of the Excellent class.
        # Will be used in predict_prob_of_excellent.
        if self.clf.classes_[0] == 'Excellent':
            self._excellent_index = 0
        else:
            self._excellent_index = 1

    @abstractmethod
    def choose_the_best_classifier(self, X_train, y_train, X_val, y_val):
        """This method choses the 'best' sklearn classifier, which
        when trained on <X_train, y_train> and performs
        the 'best' on <X_val, y_val>.
        Search over three classifiers:
        1. A BernoulliNB with default constructor.
        2. A LogisticRegression with default constructor.
        3. An SVC that has a degree 4 polynomial kernel and
        probability estimates are turned on.
        Your agent should choose the best classifier for the job.
        You should define what it means to be the 'best'.
        This method should return an untrained newly constructed
        object that is an instance of the best chosen classifier.
        OVERRIDE this method."""
        

    def predict_prob_of_excellent(self, x):
        """Given a single product, predict and return
        the probability of the product being Excellent.
        Do NOT change or override this method.       
        """
        return self.clf.predict_proba(x)[0][self._excellent_index]

class Agent_single_sklearn(Agent):
    """A baseline agent that simply uses a single classifier
    and does not search for the best classifier."""

    def __init__(self, name, clf):
        super(Agent_single_sklearn, self).__init__(name)
        self.clf = clf

    def choose_the_best_classifier(self, X_train, y_train, X_val, y_val):
        "Simply return the classifier that was provided to the constructor."
        return self.clf

