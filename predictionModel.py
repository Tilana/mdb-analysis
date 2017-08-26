import pandas as pd 
import pdb
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

stufen = ['Stufe %i' % elem for elem in range(1,11)]
features = ['gender', 'profession', 'birthyear', 'county', 'party'] + stufen


def object2Categorical(data, col):
    data[col] = data[col].astype('category')
    data[col] = data[col].cat.codes


def plotConfusionMatrix(cm, title='Confusion Matrix'):
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()


def predictionModel():

    data = pd.read_csv('clean_data_20170821.csv')


    # change to categorical values
    objColumns = data.dtypes[data.dtypes=='object'].index.tolist()
    for column in objColumns:
        if column != 'name':
            object2Categorical(data, column)


    target = data.columns[45]
    
    length = len(data)
    threshold = int(length * 0.6)

    trainX = data[features][:threshold]
    trainY = data[target][:threshold]
    testX = data[features][threshold:]
    testY = data[target][threshold:]


    model = LogisticRegression()
    model.fit(trainX, trainY)
    predY = model.predict(testX)


    print accuracy_score(testY, predY)
    confusionMatrix = confusion_matrix(testY, predY)
    plotConfusionMatrix(confusionMatrix)
    #print f1_score(testY, predY, average='macro')


    pdb.set_trace()


if __name__=='__main__':
    predictionModel()
