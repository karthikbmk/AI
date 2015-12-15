from agents import Agent
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import numpy as np

class Agent_kbangal2(Agent):
        def inaccurateSum(self,predicted,actual,predicted_proba):
                inaccurate_sum = 0

                totalMisPredictions = 0.0
                sumOfProbsOfMisPredictions = 0.0
                
                for i in range(0,len(predicted)):
                        totalMisPredictions = totalMisPredictions + 1
                        if (actual[i] == 'Trash' and predicted[i] == 'Excellent'):
                                sumOfProbsOfMisPredictions = sumOfProbsOfMisPredictions  + predicted_proba[i][0]
                        elif (actual[i] == 'Excellent' and predicted[i] == 'Trash'):
                                sumOfProbsOfMisPredictions = sumOfProbsOfMisPredictions + predicted_proba[i][1]

                return sumOfProbsOfMisPredictions
                
        
        def choose_the_best_classifier(self, X_train, y_train, X_val, y_val):
            clf = []

            bern_clf = BernoulliNB()
            bern_clf.fit(X_train, y_train)
            
            
            logi_clf = LogisticRegression()
            logi_clf.fit(X_train, y_train)
            
            svc_clf = SVC(degree=4,probability=True,random_state=0)
            svc_clf.fit(X_train, y_train)
  
            clf.append(bern_clf)
            clf.append(logi_clf)
            clf.append(svc_clf)

            bst_clf_prb = 500
            inaccurate_sum = 500
            bestClassifier = svc_clf

            x = Agent_kbangal2("kbangal2")


            for classifer in clf:
                    
                    X = classifer.predict(X_val)
                    Xprob = classifer.predict_proba(X_val)                    
                    inaccurate_sum = x.inaccurateSum(X,y_val,Xprob)
                    
                    if (inaccurate_sum) < bst_clf_prb:                            
                            bst_clf_prb = inaccurate_sum
                            bestClassifier = classifer

            best = None
            if bestClassifier == bern_clf :
                    best =  BernoulliNB()
            elif bestClassifier == logi_clf :
                    best =  LogisticRegression()
            else :
                    best = SVC(degree=4,probability=True,random_state=0)

            return best
            
                           

            
            
