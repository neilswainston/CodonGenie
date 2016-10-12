'''
PartsGenie (c) University of Manchester 2015

PartsGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import json
import os
import uuid

from flask import Flask, jsonify, request, Response

from synbiochem.utils import modify_utils, sequence_utils


# Configuration:
DEBUG = True
SECRET_KEY = str(uuid.uuid4())

# Create application:
_STATIC_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'static')
APP = Flask(__name__, static_folder=_STATIC_FOLDER)
APP.config.from_object(__name__)

_ORGANISMS = sequence_utils.get_codon_usage_organisms()


@APP.route('/')
def home():
    '''Renders homepage.'''
    return APP.send_static_file('index.html')


@APP.route('/organisms/<term>')
def get_organisms(term):
    '''Gets organisms from search term.'''
    return json.dumps([{'id': tax_id, 'name': name}
                       for name, tax_id in _ORGANISMS.iteritems()
                       if term.lower() in name.lower()])


@APP.route('/codons/', methods=['POST'])
def get_codons():
    '''Gets codons from amino_acids.'''
    query = json.loads(request.data)
    codons = modify_utils.CodonSelector().optimise_codons(query)
    return json.dumps(codons)


@APP.errorhandler(Exception)
def handle_exception(err):
    '''Exception handling method.'''
    response = jsonify({'message': err.__class__.__name__ + ': ' + str(err)})
    response.status_code = 500
    return response
