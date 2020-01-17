'''
CodonGenie (c) University of Manchester 2016

CodonGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=exec-used
import setuptools

with open('README.md', 'r') as fh:
    _LONG_DESCRIPTION = fh.read()

exec(open('codon_genie/version.py').read())  # Reads __version__

setuptools.setup(
    name='CodonGenie',
    version=__version__,
    author='Neil Swainston',
    author_email='neil.swainston@liverpool.ac.uk',
    description='CodonGenie',
    long_description=_LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/neilswainston/CodonGenie',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
