'''
Parses the files and sends them to MongoDb

Lucas Zanella, 13/02/2017
'''
from enum import Enum

c = 0
max = 50

#Strips the new line character
def cleanLine(line):
    line = line.strip('\n')
    return line

#Checks if line is WordNet comment
def isComment(line):
    if line[0] == ' ': #Comments start with empty space
        return True
    else:
        return False

def putApostrophe(string):
    return '"'+string+'"'

#Some tokens are arrays
def isArray(token):
    if token not in ['ptr_symbol', 'synset_offset']:
        return False
    else:
        return True

def removeWhitespaceAtEnd(line):
    cleanerLine = line
    max = 5
    counter = 0
    while cleanerLine[len(cleanerLine)-1] == ' ':
        cleanerLine = cleanerLine[:-1]
        counter += 1
        if counter >= max:
            break
    return cleanerLine

def arrayToJsonArray(items):
    jsonArray = '['
    comma = ''
    for index, item in enumerate(items): #https://stackoverflow.com/questions/522563/accessing-the-index-in-python-for-loops
        if not index==0:
            comma = ','
        jsonArray += comma + putApostrophe(item)
    return jsonArray + ']'


def toJson(line):
    tokens = removeWhitespaceAtEnd(line).split(' ')
    lemma = tokens[0]
    pos = tokens[1]
    synset_cnt = tokens[2]
    p_cnt = tokens[3]
    ptr_symbols = ''
    synset_offset = ''
    if p_cnt > 0:
        ptr_symbols = tokens[4:4+int(p_cnt)]
    sense_cnt = tokens[4+int(p_cnt)]
    tagsense_cnt = tokens[5+int(p_cnt)]
    synset_offset_start = 6 + int(p_cnt)
    if synset_cnt > 0:
        synset_offset = tokens[synset_offset_start:synset_offset_start+int(synset_cnt)]

    json = '{' + putApostrophe('lemma') + ":" + putApostrophe(lemma) + ',' + \
            putApostrophe('pos') + ":" + putApostrophe(pos) + ',' + \
            putApostrophe('synset_cnt') + ":" + putApostrophe(synset_cnt) + ',' + \
            putApostrophe('p_cnt') + ":" + putApostrophe(p_cnt) + ',' + \
            putApostrophe('pointers') + ":" + arrayToJsonArray(ptr_symbols) + ',' + \
            putApostrophe('sense_cnt') + ":" + putApostrophe(sense_cnt) + ',' + \
            putApostrophe('tagsense_cnt') + ":" + putApostrophe(tagsense_cnt) + ',' + \
            putApostrophe('synset_offsets') + ":" + arrayToJsonArray(synset_offset) + \
            '}'
    return json

with open('index.verb') as fp:
    for line in fp:
        if not isComment(line):
            line = cleanLine(line)
            print (toJson(line))



        c += 1
        if c > max:
            break
            #pass
