'''
CodonGenie (c) University of Manchester 2016

CodonGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import json
from urllib import request


class CodonGenieClient():
    '''CodonGenie client class.'''

    def __init__(self, url='http://codon.synbiochem.co.uk/'):
        self.__url = url if url[-1] == '/' else url + '/'

    def get_organisms(self):
        '''Get organisms.'''
        url = self.__url + 'organisms/'
        return _get_json(url)

    def search_organisms(self, term):
        '''Search organiss.'''
        url = self.__url + 'organisms/' + term
        return _get_json(url)

    def get_codons(self, amino_acids, taxonomy_id):
        '''Get codons.'''
        url = self.__url + 'codons?aminoAcids=%s&organism=%s' \
            % (amino_acids, str(taxonomy_id))
        return _get_json(url)

    def analyse(self, codon, taxonomy_id):
        '''Analyse.'''
        url = self.__url + 'codons?codon=%s&organism=%s' \
            % (codon, str(taxonomy_id))
        return _get_json(url)


def _get_json(url):
    '''Get json.'''
    with request.urlopen(url) as resp:
        data = resp.read()
        return json.loads(data)
