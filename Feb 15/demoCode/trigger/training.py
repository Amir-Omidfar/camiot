import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from joblib import dump, load


dataset = pd.read_csv("/home/pi/Desktop/trigger/imuDataAccel-26-2-20.csv")



dataset.shape
dataset.head()

#print("shape ", dataset.shape)
#print("head", dataset.head())

X = dataset.drop('Class', axis=1)
y = dataset['Class']

print("X values: ", X)
print("y values", y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier() 
classifier.fit(X_train, y_train)
dump(classifier, 'triggerTrain26-2.joblib')
print("Size of X_test",len(X_test))

y_pred = classifier.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))


