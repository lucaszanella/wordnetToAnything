'''
For each line of parsed WordNet files, save it as a new json element  

Lucas Zanella, 13/02/2017
'''

import wordnetToAnything as WN
import json

def toJson(line, kwargs):
    originalFileName = kwargs['originalFileName']
    fileObject = kwargs['fileObject']
    #We pop the counters as we don't need them in json
    if 'index' in originalFileName: #if it's an index file
        line.pop('p_cnt', None)
        line.pop('synset_cnt', None)
        line.pop('sense_cnt', None)
        line.pop('tagsense_cnt', None)
    if 'data' in originalFileName and 'wn-' not in originalFileName: #if it's a data file but not a wn-lang-data... file
        line.pop('w_cnt', None)
        line.pop('p_cnt', None)
        line.pop('sense_cnt', None)
        line.pop('tagsense_cnt', None)
    comma = ''
    newLine = '\n'
    #if not firstLine, change comma
    fileObject.write(comma + newLine + json.dumps(line))

def justPrint(line, args):
    print(line)

print('working...\n')
#Takes care of index and data files

#erases collection in case you have written something there before
originalFileName = 'index.verb'
newFileName = originalFileName + '.json'
with open(newFileName, 'w') as f:
    f.write('[')
    WN.forEachLineOfFileDo(originalFileName, 
        WN.CallbackWrapper(toJson, 
            originalFileName = originalFileName, 
            fileObject = f
        )
    )
    f.write(']')

#Takes care of data files

'''
#Takes care of MultiLingual files
language = 'pt'
fileName = 'wn-data-por.tab'
collectionName = language + '_' + replacePointWithUnderscore(fileName)
client[databaseName].drop_collection(collectionName)
WN.forEachLineOfFileDo(fileName, WN.CallbackWrapper(toMongo, fileName, collectionName))
'''