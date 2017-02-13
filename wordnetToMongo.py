'''
Parses the files and sends them to MongoDb

Lucas Zanella, 13/02/2017
'''

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

def listToJsonArray(items):
    jsonArray = '['
    comma = ''
    for index, item in enumerate(items): #https://stackoverflow.com/questions/522563/accessing-the-index-in-python-for-loops
        if not index==0:
            comma = ','
        if not type(item) is list:
            jsonArray += comma + putApostrophe(item)
        else:
            jsonArray += comma + listToJsonArray(item)
    return jsonArray + ']'

#https://wordnet.princeton.edu/wordnet/man/wndb.5WN.html#toc2
class Index(object):
    @staticmethod
    def toJson(line):
        tokens = removeWhitespaceAtEnd(line).split(' ')
        lemma = tokens[0]
        pos = tokens[1]
        synset_cnt = tokens[2]
        p_cnt = tokens[3]
        ptr_symbols = ''
        synset_offset = ''
        if int(p_cnt) > 0:
            ptr_symbols = tokens[4:4+int(p_cnt)]
        sense_cnt = tokens[4+int(p_cnt)]
        tagsense_cnt = tokens[5+int(p_cnt)]
        synset_offset_start = 6 + int(p_cnt)
        if int(synset_cnt) > 0:
            synset_offset = tokens[synset_offset_start:synset_offset_start+int(synset_cnt)]

        json = '{' + putApostrophe('lemma') + ":" + putApostrophe(lemma) + ',' + \
                putApostrophe('pos') + ":" + putApostrophe(pos) + ',' + \
                putApostrophe('synset_cnt') + ":" + putApostrophe(synset_cnt) + ',' + \
                putApostrophe('p_cnt') + ":" + putApostrophe(p_cnt) + ',' + \
                putApostrophe('pointers') + ":" + listToJsonArray(ptr_symbols) + ',' + \
                putApostrophe('sense_cnt') + ":" + putApostrophe(sense_cnt) + ',' + \
                putApostrophe('tagsense_cnt') + ":" + putApostrophe(tagsense_cnt) + ',' + \
                putApostrophe('synset_offsets') + ":" + listToJsonArray(synset_offset) + \
                '}'
        return json

#https://wordnet.princeton.edu/wordnet/man/wndb.5WN.html#toc3
class Data(object):
    @staticmethod
    def toJson(line):
        tokens = removeWhitespaceAtEnd(line).split(' ')
        synset_offset = tokens[0]
        lex_filenum = tokens[1]
        ss_type = tokens[2]
        w_cnt = tokens[3]
        #find the list [word1, lex_id1, word2, lex_id2, ...]
        words = tokens[4:4+2*int(w_cnt)]
        #returns tuple [word, lex_id] from the list [word1, lex_id1, word2, lex_id2, ...]
        words = [[words[0+n*2], words[1+n*2]] for n in range(int(len(words)/2))]
        p_cnt_index = 4+int(w_cnt)*2
        p_cnt = tokens[p_cnt_index]
        pointers = tokens[p_cnt_index+1:p_cnt_index+1+int(p_cnt)]
        json = '{' + putApostrophe('synset_offset') + ":" + putApostrophe(synset_offset) + ',' + \
                putApostrophe('lex_filenum') + ":" + putApostrophe(lex_filenum) + ',' + \
                putApostrophe('ss_type') + ":" + putApostrophe(ss_type) + ',' + \
                putApostrophe('w_cnt') + ":" + putApostrophe(w_cnt) + ',' + \
                putApostrophe('words') + ":" + listToJsonArray(words) + ',' + \
                putApostrophe('p_cnt') + ":" + putApostrophe(p_cnt) + ',' + \
                putApostrophe('pointers') + ":" + listToJsonArray(pointers) + ',' + \
                '}'
        return json

with open('data.verb') as fp:
    for line in fp:
        if not isComment(line):
            line = cleanLine(line)
            print('#################')
            print(line)
            print('-------------')
            print (Data.toJson(line))



        c += 1
        if c > max:
            break
            #pass


with open('index.verb') as fp:
    for line in fp:
        if not isComment(line):
            line = cleanLine(line)
            #print (Index.toJson(line))



        c += 1
        if c > max:
            break
            #pass
