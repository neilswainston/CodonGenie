'''
liv-utils (c) University of Liverpool. 2020

All rights reserved.

@author:  neilswainston
'''
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
import operator
import os.path
import random
import re
import tempfile
import urllib.request

from codon_genie import ncbi_tax_utils, seq_utils


AA_CODES = {'Ala': 'A',
            'Cys': 'C',
            'Asp': 'D',
            'Glu': 'E',
            'Phe': 'F',
            'Gly': 'G',
            'His': 'H',
            'Ile': 'I',
            'Lys': 'K',
            'Leu': 'L',
            'Met': 'M',
            'Asn': 'N',
            'Pro': 'P',
            'Gln': 'Q',
            'Arg': 'R',
            'Ser': 'S',
            'Thr': 'T',
            'Val': 'V',
            'Trp': 'W',
            'Tyr': 'Y',
            'Stop': '*'}


class CodonOptimiser():
    '''Class to support codon optimisation.'''

    def __init__(self, taxonomy_id):
        self.__taxonomy_id = taxonomy_id
        self.__aa_to_codon_prob = self.__get_codon_usage()
        self.__codon_prob = {item[0]: item[1]
                             for lst in self.__aa_to_codon_prob.values()
                             for item in lst}

        self.__codon_to_w = {}

        for key in self.__aa_to_codon_prob:
            aa_dict = {a: b / self.__aa_to_codon_prob[key][0][1]
                       for a, b in self.__aa_to_codon_prob[key]}
            self.__codon_to_w.update(aa_dict)

    def get_codon_prob(self, codon):
        '''Gets the codon probability.'''
        return self.__codon_prob[codon]

    def get_codon_optim_seq(self, protein_seq, excl_codons=None,
                            max_repeat_nuc=float('inf'), restr_enzyms=None,
                            max_attempts=1000, tolerant=False, stepback=3):
        '''Returns a codon optimised DNA sequence.'''
        if max_repeat_nuc == float('inf') and restr_enzyms is None:
            return ''.join([self.get_random_codon(aa, excl_codons)
                            for aa in protein_seq])

        attempts = 0
        seq = ''
        i = 0
        blockage_i = -1
        inv_patterns = 0

        while attempts < max_attempts:
            amino_acid = protein_seq[i]
            new_seq = seq + self.get_random_codon(amino_acid, excl_codons)

            invalids = seq_utils.find_invalid(new_seq, max_repeat_nuc,
                                              restr_enzyms)

            if len(invalids) == inv_patterns or \
                    (attempts == max_attempts - 1 and tolerant):

                if i == blockage_i:
                    if attempts == max_attempts - 1:
                        inv_patterns = inv_patterns + 1

                    attempts = 0

                seq = new_seq

                if i == len(protein_seq) - 1:
                    return seq

                i += 1
            else:
                blockage_i = max(i, blockage_i)
                i = max(0, (invalids[-1] // 3) - stepback)
                seq = seq[:i * 3]
                attempts += 1

        raise ValueError('Unable to generate codon-optimised sequence with '
                         '%i maximum repeating nucleotides.' % max_repeat_nuc)

    def get_cai(self, dna_seq):
        '''Gets the CAI for a given DNA sequence.'''
        w_vals = []

        for i in range(0, len(dna_seq), 3):
            codon = dna_seq[i:i + 3]

            if codon in self.__codon_to_w:
                w_vals.append(self.__codon_to_w[codon])

        return sum(w_vals) / len(w_vals)

    def mutate(self, protein_seq, dna_seq, mutation_rate):
        '''Mutate a protein-encoding DNA sequence according to a
        supplied mutation rate.'''
        return ''.join([self.get_random_codon(amino_acid)
                        if random.random() < mutation_rate
                        else dna_seq[3 * i:3 * (i + 1)]
                        for i, amino_acid in enumerate(protein_seq)])

    def get_all_codons(self, amino_acid):
        '''Returns all codons for a given amino acid.'''
        return [t[0] for t in self.__aa_to_codon_prob[amino_acid]]

    def get_best_codon(self, amino_acid):
        '''Get 'best' codon for a given amino acid.'''
        return self.__aa_to_codon_prob[amino_acid][0][0]

    def get_random_codon(self, amino_acid, excl_codons=None):
        '''Returns a random codon for a given amino acid,
        based on codon probability from the codon usage table.'''
        if excl_codons is None:
            excl_codons = []

        codon_usage = [codon_usage
                       for codon_usage in self.__aa_to_codon_prob[amino_acid]
                       if codon_usage[0] not in excl_codons]

        if not codon_usage:
            raise ValueError('No codons available for ' + amino_acid +
                             ' after excluding ' + str(excl_codons))

        while True:
            rand = random.random()
            cumulative_prob = 0

            for codon, prob in iter(reversed(codon_usage)):
                cumulative_prob += prob

                if cumulative_prob > rand:
                    return codon

    def __get_codon_usage(self):
        '''Gets the codon usage table for a given taxonomy id.'''
        aa_to_codon_prob = {aa_code: {}
                            for aa_code in AA_CODES.values()}

        url = 'http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=' \
            + str(self.__taxonomy_id) + '&aa=1&style=GCG'

        in_codons = False

        with urllib.request.urlopen(url) as resp:
            for line in resp:
                line = line.decode('utf-8').strip()

                if line == '<PRE>':
                    in_codons = True
                elif line == '</PRE>':
                    break
                elif in_codons:
                    values = re.split('\\s+', line)
                    am_acid = 'Stop' if values[0] == 'End' else values[0]

                    if am_acid in AA_CODES:
                        codon_prob = aa_to_codon_prob[AA_CODES[am_acid]]
                        codon_prob[values[1]] = float(values[3])

        aa_to_codon_prob.update((x, _scale(y))
                                for x, y in aa_to_codon_prob.items())

        return aa_to_codon_prob


def get_codon_usage_organisms(expand=False, write=False):
    '''Gets name to taxonomy id dictionary of available codon usage tables.'''
    destination = os.path.dirname(os.path.realpath(__file__))
    filename = 'expand.txt' if expand else 'normal.txt'
    filepath = os.path.join(destination, filename)

    if not os.path.exists(filepath):
        # Download:
        if not os.path.exists(destination):
            os.makedirs(destination)

        url = 'ftp://ftp.kazusa.or.jp/pub/codon/current/species.table'
        tmp = tempfile.NamedTemporaryFile(delete=False)

        urllib.request.urlretrieve(url, tmp.name)

        # Read:
        codon_orgs = _read_codon_usage_orgs_file(tmp.name)

        # Expand:
        if expand:
            new_codon_orgs = {}

            _expand_codon_usage_orgs(codon_orgs, new_codon_orgs,
                                     ncbi_tax_utils.TaxonomyFactory())

            codon_orgs = new_codon_orgs

        # Save:
        if write:
            _write_codon_usage_orgs_file(codon_orgs, filepath)

        return codon_orgs

    return _read_codon_usage_orgs_file(filepath)


def _scale(codon_usage):
    '''Scale codon usage values to add to 1.'''
    sum_cdn_usage = sum(codon_usage.values())

    if sum_cdn_usage:
        codon_usage = {key: value / sum_cdn_usage
                       for key, value in codon_usage.items()}
    else:
        codon_usage = {key: 1 / len(codon_usage)
                       for key in codon_usage}

    return sorted(codon_usage.items(), key=operator.itemgetter(1),
                  reverse=True)


def _read_codon_usage_orgs_file(filename):
    '''Reads Codon Usage Database table of species file.'''
    codon_orgs = {}

    with open(filename, 'r') as textfile:
        next(textfile)

        for line in textfile:
            tokens = line.strip().split('\t')
            codon_orgs[tokens[0]] = tokens[1]

    return codon_orgs


def _expand_codon_usage_orgs(codon_orgs, new_codon_orgs, factory,
                             max_errors=16):
    '''Expand Codon Usage Db table of species with children and synonyms.'''
    for name, tax_id in codon_orgs.items():
        errors = 0
        success = False

        while not success:
            try:
                if name and name not in new_codon_orgs:
                    new_codon_orgs[name] = tax_id

                for synonym in factory.get_names(tax_id):
                    if synonym not in new_codon_orgs:
                        new_codon_orgs[synonym] = tax_id

                _expand_codon_usage_orgs(
                    {None: child_tax_id
                     for child_tax_id in factory.get_child_ids(tax_id)},
                    new_codon_orgs, factory)

                success = True

            except ConnectionError as err:
                errors += 1

                if errors == max_errors:
                    raise err


def _write_codon_usage_orgs_file(codon_orgs, filepath):
    '''Writes Codon Usage Database table of species file.'''
    with open(filepath, 'w+') as fle:
        fle.write('Name\tId\n')

        for name, tax_id in codon_orgs.items():
            fle.write(name + '\t' + tax_id + '\n')
