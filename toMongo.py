import wordnetToAnything as WN
from pymongo import MongoClient

client = MongoClient()
databaseName = 'wordnet'

def toMongo(line, args):
    print('must insert line ' + str(line) + ' to database ' + replacePointWithUnderscore(args[0]))

def replacePointWithUnderscore(string):
    return string.replace('.','_')

#erases collection in case you have written something there before
fileName = 'index.verb'
client[databaseName].drop_collection(replacePointWithUnderscore(fileName))
WN.forEachLineOfFileDo(fileName, WN.CallbackWrapper(toMongo, fileName))
