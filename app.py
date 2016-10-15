'''
synbiochem (c) University of Manchester 2016

synbiochem is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import sys

from codon_genie import APP


def main(argv):
    '''main method.'''
    if len(argv) > 0:
        APP.run(threaded=True, port=int(argv[0]))
    else:
        APP.run(threaded=True)

if __name__ == '__main__':
    main(sys.argv[1:])
