import argparse
import sys

from pubmed_lookup import PubMedLookup, Publication


def pubmed_citation(args=sys.argv[1:], out=sys.stdout):
    """Get a citation via the command line using a PubMed ID or PubMed URL"""

    parser = argparse.ArgumentParser(
        description='Get a citation using a PubMed ID or PubMed URL')
    parser.add_argument('query', help='PubMed ID or PubMed URL')
    parser.add_argument(
        '-m', '--mini', action='store_true', help='get mini citation')
    parser.add_argument(
        '-e', '--email', action='store', help='set user email', default='')

    args = parser.parse_args(args=args)

    lookup = PubMedLookup(args.query, args.email)
    publication = Publication(lookup, resolve_doi=False)

    if args.mini:
        out.write(publication.cite_mini() + '\n')
    else:
        out.write(publication.cite() + '\n')


def pubmed_url(args=sys.argv[1:], resolve_doi=True, out=sys.stdout):
    """
    Get a publication URL via the command line using a PubMed ID or PubMed URL
    """

    parser = argparse.ArgumentParser(
        description='Get a publication URL using a PubMed ID or PubMed URL')
    parser.add_argument('query', help='PubMed ID or PubMed URL')
    parser.add_argument(
        '-d', '--doi', action='store_false', help='get DOI URL')
    parser.add_argument(
        '-e', '--email', action='store', help='set user email', default='')

    args = parser.parse_args(args=args)

    lookup = PubMedLookup(args.query, args.email)
    publication = Publication(lookup, resolve_doi=args.doi)

    out.write(publication.url + '\n')
