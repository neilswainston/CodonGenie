'''
CodonGenie (c) University of Manchester 2016

CodonGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=too-many-public-methods
import unittest

from codon_genie.client import CodonGenieClient


class Test(unittest.TestCase):
    '''Test class for client.'''

    def test_get_organisms(self):
        '''Tests get_organisms method.'''
        client = CodonGenieClient()
        organisms = client.get_organisms()

        self.assertGreater(len(organisms), 1)

    def test_search_organisms(self):
        '''Tests search_organisms method.'''
        client = CodonGenieClient()

        term = 'escherich'
        organisms = client.search_organisms(term)

        self.assertTrue(all([term.lower() in organism['name'].lower()
                             for organism in organisms]))

    def test_get_codons(self):
        '''Tests get_codons method.'''
        client = CodonGenieClient()

        codons = client.get_codons('DE', 4932)

        self.assertEqual(len(codons), 4)
        self.assertEqual(codons[0]['ambiguous_codon'], 'GAW')

    def test_analyse(self):
        '''Tests analyse method.'''
        client = CodonGenieClient()

        result = client.analyse('NTT', 4932)

        self.assertEqual(len(result[0]['amino_acids']), 4)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
