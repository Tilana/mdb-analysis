import json
import pandas as pd
import pdb

mdbFile = '../mdb-scraper/data/mdb-20170821.json'
voteFile = '../mdb-scraper/data/votes-20170821.csv'
filename = voteFile.split('-')[-1]

STUFEN = ['Stufe %i' % num for num in range(1,11)]
KEYS= ['name', 'family_name', 'gender', 'profession_group', 'children', 'state', 'martial_status', 'academic_prefix', 'honorific_prefix', 'religion', 'location'] + STUFEN 


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


def setName(data):
    data['name'] = data[['first_name', 'last_name']].apply(lambda x: ' '.join(x), axis=1)


def isMatch(name, person, data, field='last_name'):
    matches = data[data[field]==name]
    numberMatches = len(matches)
    if numberMatches == 1:
        return (True, matches.index[0])
    elif numberMatches > 1:
        fullname = person['name']
        return isMatch(fullname, person, data, 'name')
    else:
        return (False, -1)


def combineDatasets():
    personData= loadJson(mdbFile)
    persons = personData['persons']

    data = loadCSV(voteFile)
    setName(data)

    fails = []

    for person in persons:
        name = person['family_name']
        (exists, index)  = isMatch(name, person, data)
        if exists:
            setData(data, index, person)
        else:
            fails.append(person)

    print 'Number of voting data: %i' % len(data)
    print 'Number of persons searched for: % i' % len(persons)
    print '   - voting data not found: %i' % len(fails)

    data = data.dropna(subset = ['Stufe 1', 'Stufe 10'])
    print 'Number of combined data: %i' % len(data)

    data.to_csv('data_' + filename, encoding='utf8')



if __name__ == '__main__':
    combineDatasets()


