'''
liv-utils (c) University of Liverpool. 2020

All rights reserved.

@author:  neilswainston
'''
# pylint: disable=invalid-name
from collections import defaultdict
import os
import tarfile
import tempfile
import urllib


class TaxonomyFactory():
    '''Class to represent a TaxonomyFactory.'''

    def __init__(self):
        ncbi_files_dir = _get_files()
        self.__ids = _parse_nodes(os.path.join(ncbi_files_dir, 'nodes.dmp'))
        self.__names = _parse_names(os.path.join(ncbi_files_dir, 'names.dmp'))

    def get_child_ids(self, parent_id):
        '''Get child ids.'''
        child_ids = []
        self.__get_child_ids(parent_id, child_ids)
        return child_ids

    def get_names(self, tax_id):
        '''Get names.'''
        return self.__names.get(tax_id, [])

    def __get_child_ids(self, parent_id, child_ids):
        '''Get child ids.'''
        child_ids.extend(self.__ids[parent_id])

        for child_id in self.__ids[parent_id]:
            self.__get_child_ids(child_id, child_ids)


def _get_files():
    '''Get files.'''
    tmp = tempfile.NamedTemporaryFile(delete=False)
    url = 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz'
    urllib.request.urlretrieve(url, tmp.name)

    with tarfile.open(tmp.name, 'r:gz') as tr:
        temp_dir = tempfile.gettempdir()
        tr.extractall(temp_dir)
        return temp_dir


def _parse_nodes(filename):
    '''Parses nodes file.'''
    tree = defaultdict(list)

    with open(filename, 'r') as textfile:
        for line in textfile:
            tokens = [x.strip() for x in line.split('|')]
            tree[tokens[1]].append(tokens[0])

    return tree


def _parse_names(filename):
    '''Parses names file.'''
    names = defaultdict(list)

    with open(filename, 'r') as textfile:
        for line in textfile:
            tokens = [x.strip() for x in line.split('|')]
            names[tokens[0]].append(tokens[1])

    return names
