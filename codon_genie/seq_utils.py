'''
liv-utils (c) University of Liverpool. 2020

All rights reserved.

@author:  neilswainston
'''
from collections import defaultdict
import re
from Bio.Data import CodonTable
from Bio.Restriction import Restriction, Restriction_Dictionary
from Bio.Seq import Seq

NUCLEOTIDES = ['A', 'C', 'G', 'T']


NA = 'NA'
K = 'K'
TRIS = 'TRIS'
MG = 'MG'
DNTP = 'DNTP'

__DEFAULT_REAG_CONC = {NA: 0.05, K: 0, TRIS: 0, MG: 0.01, DNTP: 0}

AA_COD = defaultdict(list)

for cod, am_ac in \
        CodonTable.unambiguous_dna_by_name['Standard'].forward_table.items():
    AA_COD[am_ac].append(cod)

# ssl._create_default_https_context = ssl._create_unverified_context


def find_invalid(seq, max_repeat_nuc=float('inf'), restr_enzyms=None):
    '''Finds invalid sequences.'''
    inv = []
    seq = seq.upper()

    # Invalid repeating nucleotides:
    if max_repeat_nuc != float('inf'):
        pattern = [''.join([nucl] * (max_repeat_nuc + 1))
                   for nucl in NUCLEOTIDES]
        pattern = re.compile(r'(?=(' + '|'.join(pattern) + '))')

        inv = [m.start() for m in pattern.finditer(seq)]

    # Invalid restriction sites:
    if restr_enzyms:
        for rest_enz in [_get_restr_type(name) for name in restr_enzyms]:
            inv.extend(rest_enz.search(Seq(seq)))

    return inv


def _get_restr_type(name):
    '''Gets RestrictionType from name.'''
    types = [
        x for _, (x, y) in Restriction_Dictionary.typedict.items()
        if name in y][0]

    enz_types = tuple(getattr(Restriction, typ)
                      for typ in types)

    return Restriction.RestrictionType(
        str(name), enz_types, Restriction_Dictionary.rest_dict[name])
