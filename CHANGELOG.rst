Revision History
================

0.2.0 2016-01-22

- Create command-line tool (``pubmed-citation``) to quickly retrieve citations for PubMed IDs/URLS
- Create command-line tool (``pubmed-url``) to quickly retrieve article and DOI URLs for PubMed IDs/URLS
- Add option to save time by not resolving DOI URL (``Publication(pubmed_record, resolve_doi=False)``)
- Clean up documentation


0.1.5 2016-01-08

- Add exception for publications that do not have month information (Thanks to Sasha Cuerda!)


0.1.4 2015-12-24

- Resolve PEP8 errors
- Refactor code to be cleaner
- Configure Landscape and add code health badge
- Convert Github installation instructions to install from develop branch


0.1.3 2015-07-29

- Add tests for Publication and PubMedLookup
- Configure Travis-CI
- Configure Coveralls
- Add PyPI, Travis-CI, and Coveralls badges to README


0.1.2 2015-06-24

- Prepare for distribution via PyPI


0.1.1 2015-05-26

- Return an abbreviated citation for a Publication with cite_mini()
- Change install docs to use GitHub link, since not yet on PyPI


0.1.0 2015-05-22

- Lookup PubMed records and make Publication objects with info about a scientific publication

