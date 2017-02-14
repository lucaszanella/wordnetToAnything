import wordnetToAnything as WN
from pymongo import MongoClient

client = MongoClient()


def toMongo(line, args):
    print('must insert line ' + str(line) + ' to database ' + args[0])

client['index.verb'].drop_collection() #in case you have written something there before
WN.forEachLineOfFileDo('index.verb', WN.CallbackWrapper(toMongo, 'index.verb'))
