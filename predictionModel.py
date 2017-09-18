import pandas as pd
import numpy as np
import pdb
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn .feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt


TAGS = ['tag' + str(elem) for elem in range(1,5)]


def object2Categorical(data, col, categories):
    data[col] = data[col].astype('category')
    categories[col] = data[col].cat.categories
    data[col] = data[col].cat.codes

def flattenList(listOfList):
    return sum(listOfList, [])


def categorizeTags(data, categories):
    uniqueValues = []
    for tag in TAGS:
        uniqueValues.append(data[tag].unique().tolist())
    uniqueValues = list(set(flattenList(uniqueValues)))
    uniqueValues = [str(elem) for elem in uniqueValues]
    for tag in TAGS:
        data[tag] = data[tag].astype('category', categories = uniqueValues)
        data[tag] = data[tag].cat.codes
    categories['tags'] = uniqueValues
    return data, categories


def processTitles(data):
    titles = data['title'].tolist()
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(titles)
    vectorDF = pd.DataFrame(vectors.toarray())
    data = pd.concat([data, vectorDF], axis=1) #, left_on='level_0', right_on=0)
    return data, vectorizer


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



def getFeatureImportance(model, features, vocabulary):
    featureImportance = [(features[ind], importance) for ind, importance in enumerate(model.feature_importances_)]
    #featureImportance = [(vocabulary[ind], importance) for ind, importance in enumerate(model.feature_importances_)]
    featureImportance.sort(key=lambda x:x[1])

def predictionModel():

    data = pd.read_csv('../data/combinedData.csv')
    data.dropna(axis=0, subset=['vote'], inplace=True)
    data.reset_index(inplace=True)

    categories = {}

    data, categories = categorizeTags(data, categories)
    data, vectorizer = processTitles(data)

    objColumns = data.dtypes[data.dtypes=='object'].index.tolist()
    for column in objColumns:
        if column != 'name':
            object2Categorical(data, column, categories)


    target = 'vote'
    dropColumns = ['name', 'first_name', 'Unnamed: 0', 'index.1', 'index', 'level_0']
    dropColumns.append(target)
    features = [col for col in data.columns if col not in dropColumns]

    #pdb.set_trace()

    threshold = int(len(data)*0.6)

    #trainData = data.sample(frac=0.6, random_state=1)
    #trainData = data[:threshold]
    trainData = data[data['year'].isin([2013,2014,2015])]
    #testData = data.loc[~data.index.isin(trainData.index)]
    #testData = data[threshold:]
    testData = data[data['year'].isin([2016,2017])]

    model = LogisticRegression()
    #model = tree.DecisionTreeClassifier()
    model.fit(trainData[features], trainData[target])
    predY = model.predict(testData[features])

    print accuracy_score(testData[target], predY)
    confusionMatrix = confusion_matrix(testData[target], predY)
    print confusionMatrix
    plotConfusionMatrix(confusionMatrix, classes=categories[target], title=target)


    pdb.set_trace()


if __name__=='__main__':
    predictionModel()
