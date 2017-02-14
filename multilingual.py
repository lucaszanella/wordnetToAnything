import urllib.request
import zipfile

languages = [
    'als', 'arb', 'bul', 'cmn', 'qcn', 'dan', 'ell',
    'eng', 'fas', 'fin', 'fra', 'heb', 'hrv', 'isl',
    'ita', 'ita', 'jpn' 'cat', 'eus', 'glg', 'spa',
    'ind', 'zsm', 'nld', 'nno', 'nob', 'pol', 'por',
    'ron', 'lit', 'slk', 'slv', 'swe', 'tha'
]

baseUrl = 'http://compling.hss.ntu.edu.sg/omw/wns/'

language = 'por'
fileName = language + '.zip'
print('downloading '+fileName)
urllib.request.urlretrieve(baseUrl + language + '.zip', fileName)
print('extracting '+fileName)
with zipfile.ZipFile(fileName,"r") as zip_ref:
    zip_ref.extractall("")