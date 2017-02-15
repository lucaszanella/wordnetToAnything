'''
For each line of parsed WordNet files, save it as a new json element  

Lucas Zanella, 13/02/2017
'''

import wordnet_to_anything as WN
import json

def to_json(line, kwargs):
    """Inserts a new line into kwargs['file_object'] file object"""
    original_file_name = kwargs['original_file_name']
    file_object = kwargs['file_object']
    if 'index' in original_file_name: #if it's an index file
    #We pop the counters as we don't need them in json
        line.pop('p_cnt', None)
        line.pop('synset_cnt', None)
        line.pop('sense_cnt', None)
        line.pop('tagsense_cnt', None)
    if 'data' in original_file_name and 'wn-' not in original_file_name:
    #if it's a data file but not a wn-lang-data... file
        line.pop('w_cnt', None)
        line.pop('p_cnt', None)
        line.pop('sense_cnt', None)
        line.pop('tagsense_cnt', None)
    comma = ''
    new_line = '\n'
    #if not firstLine, change comma
    file_object.write(comma + new_line + json.dumps(line))

print('working...\n')
#Takes care of index and data files

#erases collection in case you have written something there before
original_file_name = 'index.verb'
new_file_name = original_file_name + '.json'
with open(new_file_name, 'w') as f:
    f.write('[')
    WN.forEachLineOfFileDo(original_file_name, 
        WN.CallbackWrapper(to_json, 
            original_file_name = original_file_name, 
            file_object = f
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
WN.forEachLineOfFileDo(fileName, WN.CallbackWrapper(to_json, fileName, collectionName))
'''