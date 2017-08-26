import pandas as pd 
import numpy as np
import pdb
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

stufen = ['Stufe %i' % elem for elem in range(1,11)]
features = ['gender', 'profession', 'birthyear', 'county', 'party'] + stufen


def object2Categorical(data, col, categories):
    data[col] = data[col].astype('category')
    categories[col] = data[col].cat.categories
    data[col] = data[col].cat.codes


def plotConfusionMatrix(cm, classes, title='Confusion Matrix'):
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()


def predictionModel():

    data = pd.read_csv('clean_data_20170821.csv')
    categories = {}

    objColumns = data.dtypes[data.dtypes=='object'].index.tolist()
    for column in objColumns:
        if column != 'name':
            object2Categorical(data, column, categories)


    targets = data.columns[8:127]
    for target in targets:

        print target

        trainData = data.sample(frac=0.6, random_state=1)
        testData = data.loc[~data.index.isin(trainData.index)]

        model = LogisticRegression()
        model.fit(trainData[features], trainData[target])
        predY = model.predict(testData[features])

        print accuracy_score(testData[target], predY)
        confusionMatrix = confusion_matrix(testData[target], predY)
        print confusionMatrix
        plotConfusionMatrix(confusionMatrix, classes=categories[target], title=target)


    pdb.set_trace()


if __name__=='__main__':
    predictionModel()
