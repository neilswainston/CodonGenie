'''
CodonGenie (c) University of Manchester 2016

CodonGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import sys

from codon_genie import APP


def main(argv):
    '''main method.'''
    if argv:
        APP.run(host='0.0.0.0', threaded=True, port=int(argv[0]))
    else:
        APP.run(host='0.0.0.0', threaded=True)


if __name__ == '__main__':
    main(sys.argv[1:])
