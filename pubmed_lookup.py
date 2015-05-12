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


class PubMedLookupPMID(PubMedLookup):
    """
    Retrieve a PubMed record using its PubMed ID.
    (e.g., '22331878' of 'http://www.ncbi.nlm.nih.gov/pubmed/22331878')
    """
    def __init__(self, pmid, user_email):
        super().__init__(pmid, user_email)
        self.record = self.get_pubmed_record(pmid)[0]


class PubMedLookupURL(PubMedLookup):
    """
    Retrieve a PubMed record using its PubMed URL.
    (e.g., 'http://www.ncbi.nlm.nih.gov/pubmed/22331878')
    """
    def __init__(self, pubmed_url, user_email):
        super().__init__(pubmed_url, user_email)
        pmid = self.parse_pubmed_url(pubmed_url)
        self.record = self.get_pubmed_record(pmid)[0]
