from sklearn import metrics
from Models.Algorithms import algorithms

def generateModel(X,y):
    def class_algo(model,independent,dependent):
        model.fit(independent,dependent)
        pred = model.predict(independent)
        accuracy = metrics.accuracy_score(pred,dependent)
        # print(model_name,'Accuracy : %s' % '{0:.3%}'.format(accuracy))

    
    for model_name, values in algorithms.items():
        class_algo(values["model"],X,y)