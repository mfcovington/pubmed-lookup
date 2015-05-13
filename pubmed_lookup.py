import re
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

from Bio import Entrez


class Publication(object):
    def __init__(self, pubmed_record):
        self.record = pubmed_record.record
        self.pmid = self.record['Id']
        self.title = self.record['Title']
        self.authors = ", ".join(self.record['AuthorList'])
        self.journal = self.record['Source']
        self.pub_year = re.match(r'^(?P<year>\d{4})(?:\s.+)?',
                                 self.record['PubDate']).group('year')
        self.set_article_url()
        self.set_abstract()

    def authors_et_al(self, max_authors=5):
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

    def set_abstract(self):
        """If record has an abstract, get it with PubMed ID"""
        if self.record['HasAbstract'] == 1:
            url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/' \
                  'efetch.fcgi?db=pubmed&rettype=abstract&id={}' \
                  .format(self.pmid)

            try:
                response = urlopen(url)
            except:
                abstract = ''
            else:
                xml = response.read().decode()
                abstract_pattern = r'<AbstractText[^>]*>(.+)</AbstractText>'
                abstract_matches = re.findall(abstract_pattern, xml)

            self.abstract =  "\n\n".join(abstract_matches)
        else:
            self.abstract = ''

    def set_article_url(self):
        if 'DOI' in self.record:
            doi_url = "/".join(['http://dx.doi.org', self.record['DOI']])

            try:
                response = urlopen(doi_url)
            except:
                self.url = ''
            else:
                self.url = response.geturl()
        else:
            self.url = ''


class PubMedLookup(object):
    """
    Retrieve a PubMed record using its PubMed ID or PubMed URL.
    (e.g., '22331878' OR 'http://www.ncbi.nlm.nih.gov/pubmed/22331878')
    """

    def __init__(self, query, user_email):
        Entrez.email = user_email

        pmid_pattern = r'^\d+$'
        pmurl_pattern = r'^https?://www\.ncbi\.nlm\.nih\.gov/pubmed/\d+$'
        if re.match(pmid_pattern, query):
            pmid = query
        elif re.match(pmurl_pattern, query):
            pmid = self.parse_pubmed_url(query)
        else:
            pass

        self.record = self.get_pubmed_record(pmid)[0]

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


if __name__ == '__main__':
    # NCBI will contact user by email if excessive queries are detected
    email = ''

    # Example of PubMed URL query
    url = 'http://www.ncbi.nlm.nih.gov/pubmed/11402162'
    pm1 = PubMedLookupURL(url, email)

    # Example of PubMed ID query
    pmid = '22331878'
    pm2 = PubMedLookupPMID(pmid, email)

    # Demo contents of entire record
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(pm1.record)

    # Demo extraction of record's contents
    title = pm2.record['Title']
    authors = ", ".join(pm2.record['AuthorList'])
    pub_date = pm2.record['PubDate']
    journal = pm2.record['Source']
    print(
        """
        TITLE: {}
        AUTHORS: {}
        JOURNAL: {}
        PUBDATE: {}
        ABSTRACT: {}
        URL: {}
        """
        .format(title, authors, journal, pub_date, pm2.abstract,
            pm2.url))

    publication = Publication(pm1)
    print(publication.cite())
