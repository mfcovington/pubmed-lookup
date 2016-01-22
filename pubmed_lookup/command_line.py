import argparse

from pubmed_lookup import PubMedLookup, Publication


def pubmed_citation():
    """Get a citation via the command line using a PubMed ID or PubMed URL"""

    parser = argparse.ArgumentParser(
        description='Get a citation using a PubMed ID or PubMed URL')
    parser.add_argument('query', help='PubMed ID or PubMed URL')
    parser.add_argument(
        '-m', '--mini', action='store_true', help='get mini citation')
    parser.add_argument(
        '-e', '--email', action='store', help='set user email', default='')

    args = parser.parse_args()

    lookup = PubMedLookup(args.query, args.email)
    publication = Publication(lookup, resolve_doi=False)

    if args.mini:
        print(publication.cite_mini())
    else:
        print(publication.cite())
