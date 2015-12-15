from agents import Agent

class Agent_kbangal2(Agent):

    def train(self, X, y):        
        trueProbList = []
        falseProbList = []

        noOfExcellentProds = 0
        totalNoOfProds = 0

        probE = 0.0

        for x in range(0,len(X[0])):
            trueProbList.append(0.0)
            falseProbList.append(0.0)

        for prodType in y:
            if prodType == 'Excellent':
                noOfExcellentProds = noOfExcellentProds + 1

        probE = noOfExcellentProds*1.0/len(y)        

        for row_id,featuresRow in enumerate(X):
            if y[row_id] == 'Excellent':
                for feature_id in range(0,len(X[0])):
                    if featuresRow[feature_id] == True:
                        trueProbList[feature_id] = trueProbList[feature_id] + 1
                    else:
                        falseProbList[feature_id] = falseProbList[feature_id] + 1


        for id,value in enumerate(trueProbList):
            trueProbList[id] = trueProbList[id] / noOfExcellentProds
            falseProbList[id] = falseProbList[id] / noOfExcellentProds    

        self.trueProbList = trueProbList
        self.falseProbList = falseProbList            
        self.probE = probE
        self.scalingFactor = 2**len(X[0])

    def predict_prob_of_excellent(self, x):
                
        fullyConfidentProb = 1.0
        finalProb = 1.0
        for id,featureValue in enumerate(x):
            if featureValue  == True:
                finalProb = finalProb * self.trueProbList[id]
            else:
                finalProb = finalProb * self.falseProbList[id]

        finalProb = self.probE * finalProb  * self.scalingFactor

        if finalProb > fullyConfidentProb:
            return fullyConfidentProb
        else:
            return finalProb
            
        
