import os
import sys
from setuptools import setup

if sys.version_info < (3, 3):
    print("Sorry, pubmed-lookup currently requires Python 3.3+.")
    sys.exit(1)

# From: https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    "biopython>=1.66",
    "xmltodict>=0.9.2",
]

setup(
    name='pubmed-lookup',
    version='0.2.2',
    packages=['pubmed_lookup'],
    test_suite='pubmed_lookup.test_pubmed_lookup',
    include_package_data=True,
    license='BSD License',
    keywords='citations lab literature pmid publications pubmed science',
    description='Lookup PubMed records and make Publication objects with info about a scientific publication',
    long_description=(read('README.rst') + '\n\n' +
                      read('CHANGELOG.rst')),
    url='https://github.com/mfcovington/pubmed-lookup',
    author='Michael F. Covington',
    author_email='mfcovington@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pubmed-citation=pubmed_lookup.command_line:pubmed_citation',
            'pubmed-url=pubmed_lookup.command_line:pubmed_url',
        ],
    },
)
