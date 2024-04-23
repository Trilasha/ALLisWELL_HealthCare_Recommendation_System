from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


algorithms = {'Logistic Regression':
                {"model": LogisticRegression()},

                'Decision Tree':
                {"model": tree.DecisionTreeClassifier()},

                'Random Forest':
                {"model": RandomForestClassifier()},

                'SVM':
                {"model": svm.SVC(probability=True)},

                'NaiveBayes' :
                {"model": GaussianNB()},

                'K-Nearest Neighbors' :
                {"model": KNeighborsClassifier()},
                }
