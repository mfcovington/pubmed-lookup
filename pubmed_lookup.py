import abc
import re
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

from Bio import Entrez


class PubMedLookup(metaclass=abc.ABCMeta):
    """
    This is an abstract base class for PubMed lookups.
    Don't use directly!
    """

    @abc.abstractmethod
    def __init__(self, query, user_email):
        Entrez.email = user_email

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
            abstract_pattern = r'<AbstractText>(?P<abstract>.+)</AbstractText>'
            abstract = re.search(abstract_pattern, xml).group('abstract')

        return abstract


class PubMedLookupPMID(PubMedLookup):
    """
    Retrieve a PubMed record using its PubMed ID.
    (e.g., '22331878' of 'http://www.ncbi.nlm.nih.gov/pubmed/22331878')
    """
    def __init__(self, pmid, user_email):
        super().__init__(pmid, user_email)
        self.record = self.get_pubmed_record(pmid)[0]
        if self.record['HasAbstract'] == 1:
            self.abstract = self.get_abstract(pmid)


class PubMedLookupURL(PubMedLookup):
    """
    Retrieve a PubMed record using its PubMed URL.
    (e.g., 'http://www.ncbi.nlm.nih.gov/pubmed/22331878')
    """
    def __init__(self, pubmed_url, user_email):
        super().__init__(pubmed_url, user_email)
        pmid = self.parse_pubmed_url(pubmed_url)
        self.record = self.get_pubmed_record(pmid)[0]
        if self.record['HasAbstract'] == 1:
            self.abstract = self.get_abstract(pmid)


if __name__ == '__main__':
    # NCBI will contact user by email if excessive queries are detected
    email = ''

    # Example of PubMed URL query
    url = 'http://www.ncbi.nlm.nih.gov/pubmed/22331878'
    pub1 = PubMedLookupURL(url, email)

    # Example of PubMed ID query
    pmid = '11402162'
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
    print("TITLE: {}\nAUTHORS: {}\nJOURNAL: {}\nPUBDATE: {}\nABSTRACT: {}"
        .format(title, authors, journal, pub_date, pub2.abstract))
