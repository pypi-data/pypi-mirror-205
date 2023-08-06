from ..src.DecisionTree import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier as sktree
from sklearn.tree import plot_tree
from sklearn.metrics import accuracy_score

df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/00639/Maternal%20Health%20Risk%20Data%20Set.csv",)
df.head()

d = DecisionTreeClassifier(3,1)
X = df.iloc[:, :-1]
Y = df.iloc[:, -1]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.2, random_state=41)
Y_test = Y_test.values.tolist()
Y_test = map(str, Y_test)
Y_test = list(Y_test)

df_train = pd.concat([X_train, Y_train], axis = 1)
d.fit(df_train, "RiskLevel")
Y_pred = d.predict(X_test)
a = accuracy_score(Y_test, Y_pred)

fact = df.copy()
fact["RiskLevel"] = pd.factorize(fact["RiskLevel"])[0]
# 0 = high risk
# 1 = low risk
# 2 = mid risk
X2 = fact.iloc[:, :-1]
Y2 = fact.iloc[:, -1]
X2_train, X2_test, Y2_train, Y2_test = train_test_split(X2, Y2, test_size=.2, random_state=41)
clf = sktree(max_depth = 3)
clf = clf.fit(X2_train, Y2_train)
Y2_pred = clf.predict(X2_test)
b = accuracy_score(Y2_test, Y2_pred)

print("Implementation: ", round(a*100, 2), "\nScikitLearn: ", round(b*100, 2))

#Second Test
df2 = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data",
                 names = ["classes","cap-shape", "cap-surface", "cap-color", "bruises", "odor", "gill-attachment", "gill-spacing", "gill-size", "gill-color","stalk-shape","stalk-root","stalk-surface-above-ring","stalk-surface-below-ring","stalk-color-above-ring","stalk-color-below-ring","veil-type","veil-color","ring-number","ring-type","spore-print-color","population","habitat"])
df2.head()

d2 = DecisionTreeClassifier(3,1)
X3 = df2.iloc[:, 1:]
Y3 = df2.iloc[:, 0]
X3train, X3test, Y3train, Y3test = train_test_split(X3, Y3, test_size=.2, random_state = 27)
Y3test = Y3test.values.tolist()
Y3test = map(str, Y3test)
Y3test = list(Y3test)
df2_train = pd.concat([X3train, Y3train], axis = 1)
d2.fit(df2_train, "classes")
Y3pred = d2.predict(X3test)
a2 = accuracy_score(Y3test, Y3pred)

fact2 = df2.copy()
fact2 = fact2.apply(lambda x: pd.factorize(x)[0])
X4 = fact2.iloc[:, 1:]
Y4 = fact2.iloc[:, 0]
X4_train, X4_test, Y4_train, Y4_test = train_test_split(X4, Y4, test_size=.2, random_state=41)

clf = sktree(max_depth = 2)
clf = clf.fit(X4_train, Y4_train)
Y4_pred = clf.predict(X4_test)
b2 = accuracy_score(Y4_test, Y4_pred)
print("Implementation: ", round(a2*100, 2), "\nScikitLearn: ", round(b2*100, 2))
