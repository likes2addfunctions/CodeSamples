### This is a tool to perform gradient descent on a single varible.
# Based on Andrew Ng's Machine Learning course at Stanford

import random
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go


def hTheta(t0, t1, x):
    return t0 + t1*x

### Cost Function
def JTheta(t0, t1, x,y):
    cost = 0
    for k in range(len(x)):
        cost = cost + (hTheta(t0,t1,x[k]) - y[k])**2
    cost = cost/(2*NumOfVars)    

### Run Gradient Descent


def GradDescent(t0,t1,y,x,a, iterations):
    t0s = []
    t1s = []
    for i in range(iterations):
        DJ0 = 0
        for k in range(len(x)):
            DJ0 = DJ0 + (hTheta(t0,t1,x[k]) - y[k])
        DJ0 = DJ0/(NumOfVars)
        DJ1 = 0
        for k in range(len(x)):
            DJ1 = DJ1 + (hTheta(t0,t1,x[k]) - y[k])*x[k]
        DJ1 = DJ1/(NumOfVars)        
        t0 = t0 - a*DJ0
        t1 = t1 - a*DJ1

        t0s = t0s + [t0]
        t1s = t1s + [t1]

    
    printstr = "y = " + str(t0) + " + " + str(t1) + "x"
    print printstr
    predictedY = []
    for x in XVect:
        predictedY = predictedY + [t0 + t1*x]
    fig = plt.figure()
    scatter = fig.add_subplot(211)
    scatter.set_title('Iterations vs. Coefficient Values') 
    plt.plot(range(iterations), t0s)
    plt.plot(range(iterations), t1s)
    
    iterations = fig.add_subplot(212)
    plt.plot(XVect,predictedY, 'r')
    plt.scatter(XArray,YArray)
    fig.show()
    print list(XArray)
    print list(YArray)
    return (t0,t1)
    
NumOfVars = 1

### Generates pseudo random linear data

Data = []
m = 20 * random.random() - 10
randscalex = 5*random.random()
randscaley = 5*random.random()
randscalez = 5*random.random()
for i in range(50):
    x = randscalex * random.random() - 1
    y = randscaley * random.random() - 1
    z = randscalez * random.random() -1
    Data = Data + [[m*x + y, x + z]]

### Create Arrays and Vectors for graphing
    
XVect = []
YVect = []
for k in range(len(Data)):
    XVect = XVect + [Data[k][1]]
    YVect = YVect + [Data[k][0]]

XArray = np.array(XVect)
YArray = np.array(YVect)

### Linear Regression Hypothesis
Theta0 = 1
Theta1 = 1


GradDescent(Theta0,Theta1,YVect,XVect,.001,100)
#
#
#plt.show()

### Calculates means for each variable
#MeanVector = []
#
#for k in range(len(Data[0])):
#    Mean = 0 
#    for sample in Data:
#	Mean  = Mean + sample[k]
#    Mean = Mean/(len(Data))
#    MeanVector = MeanVector + [Mean]
#MeanVector = numpy.array[MeanVector]
#print MeanVector
#
#residuals = []
#for sample in Data:
#	residuals = residuals + [sample[0] - Mean]
#residuals = numpy.array(residuals)
#print residuals
#alpha = .1



