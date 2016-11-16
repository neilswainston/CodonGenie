'''
CodonGenie (c) University of Manchester 2016

CodonGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=bad-builtin
# pylint: disable=too-few-public-methods
from collections import defaultdict
import itertools

from synbiochem.utils import sequence_utils
from synbiochem.utils.sequence_utils import CodonOptimiser
import Bio.Data.CodonTable as CodonTable


class CodonSelector(object):
    '''Class to optimise codon selection.'''

    def __init__(self, table_id=1, wanted_pen=3, degen_pen=-1, unwanted_pen=-3,
                 stop_pen=-10):
        self.__codon_to_aa = \
            CodonTable.unambiguous_dna_by_id[table_id].forward_table
        self.__aa_to_codon = defaultdict(list)

        self.__wanted_pen = wanted_pen
        self.__degen_pen = degen_pen
        self.__unwanted_pen = unwanted_pen
        self.__stop_pen = stop_pen

        for codon, amino_acid in self.__codon_to_aa.iteritems():
            self.__aa_to_codon[amino_acid].append(codon)

        self.__codon_opt = {}

    def optimise_codons(self, amino_acids, organism_id):
        '''Optimises codon selection.'''
        req_amino_acids = set(amino_acids.upper())

        codons = [sequence_utils.CODONS[amino_acid]
                  for amino_acid in req_amino_acids]

        combos = [combo for combo in itertools.product(*codons)]

        results = [self.__analyse(combo, organism_id, req_amino_acids)
                   for combo in combos]

        return self.__format_results(results)

    def analyse_codon(self, ambig_codon, tax_id):
        '''Analyses an ambiguous codon.'''
        results = [[self.__analyse_codon(ambig_codon.upper(), tax_id)]]
        return self.__format_results(results)

    def __analyse(self, combo, tax_id, req_amino_acids):
        '''Analyses a combo, returning nucleotides, ambiguous nucleotides,
        amino acids encodes, and number of variants.'''
        transpose = [sorted(list(term)) for term in map(set, zip(*combo))]

        nucls = [[''.join(sorted(list(set(pos))))]
                 for pos in transpose[:2]] + [_optimise_pos_3(transpose[2])]

        ambig_codons = [''.join([sequence_utils.NUCL_CODES[term]
                                 for term in cdn])
                        for cdn in itertools.product(*nucls)]

        results = [self.__analyse_codon(ambig_codon, tax_id, req_amino_acids)
                   for ambig_codon in ambig_codons]

        return results

    def __get_codon_opt(self, tax_id):
        '''Gets the CodonOptimiser for the supplied taxonomy.'''
        if tax_id not in self.__codon_opt:
            self.__codon_opt[tax_id] = CodonOptimiser(tax_id)

        return self.__codon_opt[tax_id]

    def __analyse_codon(self, ambig_codon, tax_id, req_amino_acids=None):
        '''Analyses a given ambiguous codon.'''
        if req_amino_acids is None:
            req_amino_acids = []

        codon_opt = self.__get_codon_opt(tax_id)

        ambig_codon_nucls = [sequence_utils.INV_NUCL_CODES[nucl]
                             for nucl in ambig_codon]

        codons = [''.join(c) for c in itertools.product(*ambig_codon_nucls)]

        amino_acids = defaultdict(list)

        for codon in codons:
            a_a = self.__codon_to_aa.get(codon, 'Stop')
            amino_acids[a_a].append((codon,
                                     codon_opt.get_codon_prob(codon)))

        result = (ambig_codon,
                  tuple(ambig_codon_nucls),
                  tuple(codons),
                  tuple([(key, tuple(sorted(value,
                                            key=lambda prob: prob[1],
                                            reverse=True)))
                         for key, value in amino_acids.iteritems()]),
                  self.__score(amino_acids, req_amino_acids),
                  )

        return result

    def __score(self, amino_acids, req_amino_acids):
        '''Scores a given amino acids collection.'''
        if len(req_amino_acids) == 0:
            return 0

        scores = [value[1]
                  for amino_acid, values in amino_acids.iteritems()
                  for value in values
                  if amino_acid in req_amino_acids]

        return sum(scores) / float(len(scores))

    def __format_results(self, results):
        '''Formats results.'''
        results = list(set([codon for result in results for codon in result]))
        results.sort(key=lambda x: (len(x[2]), -x[4]))
        return results


def _optimise_pos_3(options):
    options = list(set([tuple(sorted(set(opt)))
                        for opt in itertools.product(*options)]))
    options.sort(key=len)
    return [''.join(opt) for opt in options]
