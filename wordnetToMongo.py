'''
Parses the files and sends them to MongoDb

Lucas Zanella, 13/02/2017
'''
import json

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
        synset_offsets = ''
        if int(p_cnt) > 0:
            ptr_symbols = tokens[4:4+int(p_cnt)]
        sense_cnt = tokens[4+int(p_cnt)]
        tagsense_cnt = tokens[5+int(p_cnt)]
        synset_offset_start = 6 + int(p_cnt)
        if int(synset_cnt) > 0:
            synset_offsets = tokens[synset_offset_start:synset_offset_start+int(synset_cnt)]
        return {
            'lemma': lemma,
            'synset_cnt': synset_cnt,
            'p_cnt': p_cnt,
            'pointers': ptr_symbols,
            'sense_cnt': sense_cnt,
            'tagsense_cnt': tagsense_cnt,
            'synset_offsets': synset_offsets
        }

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
        words = [{'word': words[0+n*2], 'lex_id': words[1+n*2]} for n in range(int(len(words)/2))]
        p_cnt_index = 4+int(w_cnt)*2
        p_cnt = tokens[p_cnt_index]
        #find the list [pointer1, pointer2, ...] where each pointer object is composed
        #of [pointer_symbol, synset_offset, pos, source_target]
        pointers = tokens[p_cnt_index+1:p_cnt_index+1+int(p_cnt)*4]
        pointers = [
            {
                'pointer_symbol': pointers[0+n*4],
                'synset_offset': pointers[1+n*4],
                'pos': pointers[2+n*4],
                'source_target': pointers[3+n*4]
            }
            for n in range(int(len(pointers)/4))
        ]
        return {
            'synset_offset': synset_offset,
            'lex_filenum': lex_filenum,
            'ss_type': ss_type,
            'w_cnt': w_cnt,
            'words': words,
            'p_cnt': p_cnt,
            'pointers': pointers
        }

with open('data.verb') as fp:
    for line in fp:
        if not isComment(line):
            line = cleanLine(line)
            print('#################')
            print(line)
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
