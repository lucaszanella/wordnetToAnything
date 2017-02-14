import wordnetToAnything as WN
from pymongo import MongoClient

client = MongoClient()

#forEachLineOfFileDo('data.verb', print)

def toMongo(line, args):
    print('must insert line ' + str(line) + ' to database ' + args[0])

#db.drop_collection('index.verb')
WN.forEachLineOfFileDo('index.verb', WN.CallbackWrapper(toMongo, 'index.verb'))
