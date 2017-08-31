# -*- coding: utf-8 -*-

import pandas as pd
from ast import literal_eval 
import pdb
import numpy as np

PATH = '../data/Abstimmungen.csv'
NR_TAGS = 4


def string2list(string):
    string = string.replace('[','')
    string = string.replace(']','')
    return [elem.strip() for elem in string.split(',')]

def date2year(datum):
    return datum.split(' ')[-1]

def date2month(datum):
    return datum.split(' ')[-2]


def processAbstimmungsData():

    votingData = pd.read_csv(PATH)

    # Split and reduce number of tags
    tags = votingData['tags']
    tagList = [string2list(tag) for tag in tags.tolist()]
    tagList = [tags[:NR_TAGS] for tags in tagList]
    tagNames = ['tag%i' % elem for elem in range(1,5)]
    tagDF = pd.DataFrame(tagList, columns=tagNames)

    votingData = pd.concat([votingData, tagDF], axis=1)

    # Split date into a year and month column
    votingData['year'] = votingData['datum'].apply(date2year)
    votingData['month'] = votingData['datum'].apply(date2month)


    # Remove redundant columns
    dropCols = ['Unnamed: 0', 'csv', 'directory', 'legislaturperiode', 'categories', 'tags', 'datum']
    votingData = votingData.drop(dropCols, axis=1)

    votingData.to_csv('../data/cleanAbstimmungen.csv', encoding='utf8')


if __name__=='__main__':
    processAbstimmungsData()
