'''
PartsGenie (c) GeneGenie Bioinformatics Ltd. 2020

All rights reserved.

@author:  neilswainston
'''
import random
import unittest

from codon_genie import codon_utils
from utils import seq_utils


class CodonOptimiserTest(unittest.TestCase):
    '''Test class for CodonOptimiser.'''

    def test_get_codon_prob(self):
        '''Tests get_codon_prob method.'''
        cod_opt = codon_utils.CodonOptimiser('83333')
        self.assertAlmostEqual(0.46, cod_opt.get_codon_prob('CTG'), 2)

    def test_get_codon_optim_seq(self):
        '''Tests get_codon_optim_seq method.'''
        cod_opt = codon_utils.CodonOptimiser('83333')
        aa_codes = seq_utils.AA_CODES
        aa_codes.pop('Stop')

        aa_seq = ''.join([random.choice(list(aa_codes.values()))
                          for _ in range(random.randint(100, 2500))])

        max_repeat_nuc = 5
        restr_enzyms = ['BsaI']
        dna_seq = cod_opt.get_codon_optim_seq(aa_seq,
                                              max_repeat_nuc=max_repeat_nuc,
                                              restr_enzyms=restr_enzyms)

        self.assertFalse(seq_utils.is_invalid(dna_seq, max_repeat_nuc,
                                              restr_enzyms))

    def test_get_random_codon(self):
        '''Tests get_random_codon method.'''
        cod_opt = codon_utils.CodonOptimiser('83333')
        self.assertEqual('CTA', cod_opt.get_random_codon('L', ['CTG', 'TTA',
                                                               'CTT', 'TTG',
                                                               'CTC']))

    def test_get_random_codon_fail(self):
        '''Tests get_random_codon method.'''
        cod_opt = codon_utils.CodonOptimiser('83333')
        self.assertRaises(
            ValueError, cod_opt.get_random_codon, 'M', ['ATG'])


class Test(unittest.TestCase):
    '''Test class for codon_utils module.'''

    def test_get_codon_usage_organisms_normal(self):
        '''Tests get_random_codon method.'''
        organisms = codon_utils.get_codon_usage_organisms()
        self.assertIn('Escherichia coli', organisms)

    def test_get_codon_usage_organisms_expand(self):
        '''Tests get_random_codon method.'''
        organisms = codon_utils.get_codon_usage_organisms(expand=True)
        self.assertIn('Escherichia coli', organisms)


if __name__ == "__main__":
    unittest.main()
