'''
CodonGenie (c) University of Manchester 2016

CodonGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from codon_genie.client import CodonGenieClient


def seq_from_alignment(alignment, tax_id):
    '''Generates a DNA sequence from amino acid sequence alignment.'''
    dna_seq = ''

    client = CodonGenieClient()

    # Loop over each position in the alignment:
    for position in zip(*[list(seq) for seq in alignment]):
        # For each position, generate set of amino acids, ignoring inserts:
        amino_acids = ''.join({pos for pos in position if pos != '-'})

        # Query CodonGenie webservice with set of amino acids, to determine
        # optimum ambiguous codon for this position:
        for codon in client.get_codons(amino_acids, tax_id):
            # Add first (best scoring) ambigous codon to the DNA sequence:
            dna_seq += codon['ambiguous_codon']
            break

    return dna_seq


def _get_tax_id(organism_name):
    '''Gets NCBI Taxonomy id from organism name.'''
    # Query CodonGenie webservice with organism name:
    client = CodonGenieClient()

    for organism in client.search_organisms(organism_name):
        return organism['id']

    raise ValueError(organism_name + ' not found')


if __name__ == '__main__':
    print(seq_from_alignment(['PFDMR', 'PIAMR', 'PLHLR', 'PMNMR', 'PVHMR'],
                             _get_tax_id('Escherichia coli')))
