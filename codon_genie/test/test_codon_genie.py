'''
CodonGenie (c) GeneGenie Bioinformatics Ltd. 2020

All rights reserved.

@author:  neilswainston
'''
# pylint: disable=too-many-public-methods
import unittest

from codon_genie.codon_genie import CodonSelector


class Test(unittest.TestCase):
    '''Test class for codon_utils.'''

    def test_optimise_codons(self):
        '''Tests optimise_codons method.'''
        cod_sel = CodonSelector()
        codons = cod_sel.optimise_codons('FLIMV', '37762')

        self.assertEqual(len(codons), 12)
        self.assertEqual(codons[0]['ambiguous_codon'], 'DTK')


if __name__ == '__main__':
    unittest.main()
