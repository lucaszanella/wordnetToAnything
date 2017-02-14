'''
For each line of parsed WordNet files, send it to MongoDB

Lucas Zanella, 13/02/2017
'''

import wordnetToAnything as WN
from pymongo import MongoClient

client = MongoClient()
databaseName = 'wordnet'

def toMongo(line, args):
    fileName = args[0]
    collectionName = args[1]
    #We pop the counters as we don't need them in json
    if 'index' in fileName: #if it's an index file
        line.pop('p_cnt', None)
        line.pop('synset_cnt', None)
        line.pop('sense_cnt', None)
        line.pop('tagsense_cnt', None)
    client[databaseName][collectionName].insert_one(line)

def replacePointWithUnderscore(string):
    return string.replace('.','_')

def justPrint(line, args):
    print(line)

print('working...\n')
#Takes care of index files
'''
#erases collection in case you have written something there before
fileName = 'index.verb'
collectionName = replacePointWithUnderscore(fileName)
client[databaseName].drop_collection(collectionName)
WN.forEachLineOfFileDo(fileName, WN.CallbackWrapper(toMongo, fileName, collectionName))
'''
#Takes care of data files

#Takes care of MultiLingual files
language = 'pt'
fileName = 'wn-data-por.tab'
collectionName = language + '_' + replacePointWithUnderscore(fileName)
client[databaseName].drop_collection(collectionName)
WN.forEachLineOfFileDo(fileName, WN.CallbackWrapper(toMongo, fileName, collectionName))