import abc
import re
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

from Bio import Entrez


class Publication(object):
    def __init__(self, pubmed_record):
        self.record = pubmed_record.record
        self.title = self.record['Title']
        self.authors = ", ".join(self.record['AuthorList'])
        self.journal = self.record['Source']
        self.abstract = pubmed_record.abstract
        self.url = pubmed_record.url
        self.pub_year = re.match(r'^(?P<year>\d{4})(?:\s.+)?',
                                 self.record['PubDate']).group('year')

    def authors_et_al(self, max_authors):
        author_list = self.record['AuthorList']
        if len(author_list) <= max_authors:
            authors_et_al = self.authors
        else:
            authors_et_al = ", ".join(
                self.record['AuthorList'][:max_authors]) + ", et al."
        return authors_et_al

    def cite(self, max_authors=5):
        citation_data = {
            'title': self.title,
            'authors': self.authors_et_al(max_authors),
            'year': self.pub_year,
            'journal': self.journal,
            'volume': self.record['Volume'],
            'issue': self.record['Issue'],
            'pages': self.record['Pages'],
        }
        return "{authors} ({year}). {title} {journal} {volume}({issue}): {pages}." \
            .format(**citation_data)


class PubMedLookup(metaclass=abc.ABCMeta):
    """
    This is an abstract base class for PubMed lookups.
    Don't use directly!
    """

    @abc.abstractmethod
    def __init__(self, query, user_email):
        Entrez.email = user_email

    def pubmed_query(self, pmid):
        self.record = self.get_pubmed_record(pmid)[0]

        if 'DOI' in self.record:
            self.get_article_url()
        else:
            self.url = ''

        if self.record['HasAbstract'] == 1:
            self.abstract = self.get_abstract(pmid)
        else:
            self.abstract = ''

    def get_article_url(self):
        doi_url = "/".join(['http://dx.doi.org', self.record['DOI']])

        try:
            response = urlopen(doi_url)
        except:
            self.url = ''
        else:
            self.url = response.geturl()

    @staticmethod
    def parse_pubmed_url(pubmed_url):
        """Get PubMed ID (pmid) from PubMed URL."""
        parse_result = urlparse(pubmed_url)
        pattern = re.compile('^/pubmed/(\d+)$')
        pmid = pattern.match(parse_result.path).group(1)
        return pmid

    @staticmethod
    def get_pubmed_record(pmid):
        """Get PubMed record from PubMed ID."""
        handle = Entrez.esummary(db="pubmed", id=pmid)
        record = Entrez.read(handle)
        return record

    @staticmethod
    def get_abstract(pmid):
        """Get abstract from PubMed ID"""
        url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/' \
              'efetch.fcgi?db=pubmed&rettype=abstract&id={}'.format(pmid)

        try:
            response = urlopen(url)
        except:
            abstract = ''
        else:
            xml = response.read().decode()
            abstract_pattern = r'<AbstractText[^>]*>(.+)</AbstractText>'
            abstract_matches = re.findall(abstract_pattern, xml)

        return "\n\n".join(abstract_matches)


class PubMedLookupPMID(PubMedLookup):
    """
    Retrieve a PubMed record using its PubMed ID.
    (e.g., '22331878' of 'http://www.ncbi.nlm.nih.gov/pubmed/22331878')
    """
    def __init__(self, pmid, user_email):
        super().__init__(pmid, user_email)
        self.pubmed_query(pmid)


class PubMedLookupURL(PubMedLookup):
    """
    Retrieve a PubMed record using its PubMed URL.
    (e.g., 'http://www.ncbi.nlm.nih.gov/pubmed/22331878')
    """
    def __init__(self, pubmed_url, user_email):
        super().__init__(pubmed_url, user_email)
        pmid = self.parse_pubmed_url(pubmed_url)
        self.pubmed_query(pmid)


if __name__ == '__main__':
    # NCBI will contact user by email if excessive queries are detected
    email = ''

    # Example of PubMed URL query
    url = 'http://www.ncbi.nlm.nih.gov/pubmed/11402162'
    pub1 = PubMedLookupURL(url, email)

    # Example of PubMed ID query
    pmid = '22331878'
    pub2 = PubMedLookupPMID(pmid, email)

    # Demo contents of entire record
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(pub1.record)

    # Demo extraction of record's contents
    title = pub2.record['Title']
    authors = ", ".join(pub2.record['AuthorList'])
    pub_date = pub2.record['PubDate']
    journal = pub2.record['Source']
    print(
        """
        TITLE: {}
        AUTHORS: {}
        JOURNAL: {}
        PUBDATE: {}
        ABSTRACT: {}
        URL: {}
        """
        .format(title, authors, journal, pub_date, pub2.abstract,
            pub2.url))
