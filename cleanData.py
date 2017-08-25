# -*- coding: utf-8 -*-
import pandas as pd
import re

PATH = 'data_20170821.csv'
STUFEN = ['Stufe %i' % elem for elem in range(1,11)]


def removeGender(text):
    text = re.sub('in ', ' ', text)
    text = re.sub('in$', '', text) 
    return text.replace('frau', 'mann')

def removeAcademicDegree(text):
    return re.sub('(Dipl)+(\.)*(-)*(om)*(-)*', '', text)

def removeStudies(text):
    text = re.sub('Studium (der)*', '', text)
    text = re.sub('Promovierte(r)* ', '', text)
    text = re.sub('Staatl. Gepr. ', '', text)
    text = re.sub(' für .*', '', text)
    return text


def removeParenthesis(text):
    return re.sub('\(.*\)', '', text)

def takeFirstJob(text):
    text = text.split(',')[0]
    text = text.split(';')[0]
    return text.split('/')[0]

def correctEnding(text):
    text = re.sub('log$', 'loge', text)
    text = re.sub('gog$', 'goge', text)
    text = re.sub('ärtz$', 'arzt', text)
    text = re.sub('wält$', 'walt', text)
    return text

def upperCase(text):
    return text.title()


def stripText(text):
    return text.strip()


def categorizeJobs(data, col):
    data[col] = data[col].apply(takeFirstJob)
    data[col] = data[col].apply(stripText)
    data[col] = data[col].apply(removeGender)
    data[col] = data[col].apply(removeAcademicDegree)
    data[col] = data[col].apply(removeParenthesis)
    data[col] = data[col].apply(removeStudies)
    data[col] = data[col].apply(removeStudies)
    data[col] = data[col].apply(correctEnding)
    data[col] = data[col].apply(upperCase)
    data[col] = data[col].apply(stripText)


def name2number(elem):
    try:
        return int(elem)
    except:
        return 1


def object2Categorical(data, col):
    data[col] = data[col].astype('category')



def cleanData():

    data = pd.read_csv(PATH)

    # remove first and last name
    data = data.drop(['first_name', 'last_name', 'family_name'], axis=1)

    # Replace NAN values
    data.fillna('-', inplace=True)

    # change company names in salaries ranges to number
    for stufe in STUFEN:
        data[stufe] = data[stufe].apply(name2number)


    # categorize education and professions
    categorizeJobs(data, 'education')
    categorizeJobs(data, 'profession')


    # Fix types - birthyear 1067
    data.birthyear[data.birthyear < 1900] = 1967

    # change to categorical values
    objColumns = data.dtypes[data.dtypes=='object'].index.tolist()
    for column in objColumns:
        if column != 'name':
            object2Categorical(data, column)


    data.to_csv('clean_' + PATH)




if __name__ == '__main__':
    cleanData()
