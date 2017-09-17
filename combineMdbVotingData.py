import json
import pandas as pd
import pdb

PATH = '../data/'
mdbFile = PATH + 'MdB.json'
voteFile = PATH + 'mdbAbstimmungen.csv'
voteDetailsFile = PATH + 'cleanAbstimmungen.csv'

STUFEN = ['Stufe %i' % num for num in range(1,11)]
KEYS= ['gender', 'state', 'academic_prefix', 'honorific_prefix', 'religion'] + STUFEN


def loadJson(path):
    with open(path) as data_file:
        return json.load(data_file)


def loadCSV(path):
    return pd.DataFrame.from_csv(path)


def setData(data, ind, person):
    for key in KEYS:
        try:
            value = person[key]
            if isinstance(value, list):
                value = len(value)
        except:
            value = '-'
        data.loc[ind, key] = value


def isMatch(name, person, data, field='name'):
    matches = data[data[field]==name.encode('utf8')]
    numberMatches = len(matches)
    if numberMatches == 1:
        return (True, matches.index[0])
    elif numberMatches > 1:
        firstName = person['given_name'].encode('utf8')
        fullnameMatch = matches[matches['first_name']==firstName]
        if len(fullnameMatch) == 1:
            return (True, fullnameMatch.index[0])
        else:
            return (False, -1)
    else:
        return (False, -1)


def combineMdbVotingData():
    personData= loadJson(mdbFile)
    persons = personData['persons']

    voteData = loadCSV(voteFile)
    voteDetails = loadCSV(voteDetailsFile)
    voteDetails.drop_duplicates(inplace=True)
    fails = []

    for person in persons:
        name = person['family_name']
        (exists, index)  = isMatch(name, person, voteData)
        if exists:
            setData(voteData, index, person)
        else:
            print 'WARNING: %s  %s not found' % (person['given_name'], person['family_name'])
            fails.append(person)

    print '---------'
    print 'Number of voting data: %i' % len(voteData)
    print 'Number of MDb data: % i' % len(persons)
    print '   - Number of name mismatches: %i' % len(fails)

    voteData = voteData.dropna(subset = ['Stufe 1', 'Stufe 10'])
    print 'Number of combined data: %i' % len(voteData)


    print '--------'

    voteTitles = [column for column in voteData.columns if 'Abstimmung:' in column]
    columnNames = [(title, title.split('_')[0]) for title in voteTitles]
    voteData = voteData.rename(columns = dict(columnNames))
    voteData.reset_index(inplace=True)
    voteTitles = [column for column in voteData.columns if 'Abstimmung:' in column]

    data = []

    for voteTitle in voteTitles:
        details = voteDetails[voteDetails.title == voteTitle]
        try:
            details = details.append([details] * (len(voteData)-1))
            details.reset_index(inplace=True)

            combinedData = pd.concat([details, voteData], axis=1)
            combinedData['vote'] = voteData[voteTitle]
            combinedData = combinedData.drop(voteTitles, axis=1)
            data.append(combinedData)
        except:
            print 'Multiple voting data found'
            print voteTitle
            print ''

    data = pd.concat(data)
    data.to_csv(PATH + 'combinedData.csv', encoding='utf8')



if __name__ == '__main__':
    combineMdbVotingData()


