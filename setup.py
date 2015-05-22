import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    "biopython>=1.65",
    "xmltodict>=0.9.2",
]

setup(
    name='pubmed-lookup',
    version='0.0.0',
    packages=['pubmed_lookup'],
    include_package_data=True,
    license='BSD License',
    description='Lookup PubMed records and make Publication objects with info about a scientific publication',
    long_description=README,
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
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=install_requires,
)
