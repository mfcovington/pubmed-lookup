import re
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

from Bio import Entrez
import xmltodict


class Publication(object):
    """
    Use a PubMedLookup record to make a Publication object with info about
    a scientific publication.
    """
    def __init__(self, pubmed_record):
        """
        Upon init: set Publication attributes (record, pmid, pubmed_url,
        title, authors, journal, pub_year, url, and abstract)
        """
        self.record = pubmed_record.record
        self.pmid = self.record['Id']
        self.pubmed_url = 'http://www.ncbi.nlm.nih.gov/pubmed/{}' \
                          .format(self.pmid)
        self.title = self.record['Title']
        self.authors = ", ".join(self.record['AuthorList'])
        self.journal = self.record['Source']
        self.pub_year = re.match(r'^(?P<year>\d{4})(?:\s.+)?',
                                 self.record['PubDate']).group('year')
        self.volume = self.record['Volume']
        self.issue = self.record['Issue']
        self.pages = self.record['Pages']
        self.set_article_url()
        self.set_abstract()

    def authors_et_al(self, max_authors=5):
        """
        Return string with a truncated author list followed by 'et al.'
        """
        author_list = self.record['AuthorList']
        if len(author_list) <= max_authors:
            authors_et_al = self.authors
        else:
            authors_et_al = ", ".join(
                self.record['AuthorList'][:max_authors]) + ", et al."
        return authors_et_al

    def cite(self, max_authors=5):
        """
        Return string with a citation for the record, formatted as:
        '{authors} ({year}). {title} {journal} {volume}({issue}): {pages}.'
        """
        citation_data = {
            'title': self.title,
            'authors': self.authors_et_al(max_authors),
            'year': self.pub_year,
            'journal': self.journal,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
        }
        citation = "{authors} ({year}). {title} {journal}".format(**citation_data)
        if self.volume and self.issue and self.pages:
            citation += " {volume}({issue}): {pages}.".format(**citation_data)
        elif self.volume and self.issue:
            citation += " {volume}({issue}).".format(**citation_data)
        elif self.volume and self.pages:
            citation += " {volume}: {pages}.".format(**citation_data)
        elif self.volume:
            citation += " {volume}.".format(**citation_data)
        elif self.pages:
            citation += " {pages}.".format(**citation_data)
        else:
            citation += "."

        return citation

    @staticmethod
    def parse_abstract(xml):
        abstract_paragraphs = []
        xml_dict = xmltodict.parse(xml)
        abstract_xml = xml_dict['PubmedArticleSet']['PubmedArticle'] \
            ['MedlineCitation']['Article']['Abstract']['AbstractText']

        if isinstance(abstract_xml, str):
            abstract_paragraphs.append(abstract_xml)

        elif isinstance(abstract_xml, dict):
            abstract_text = abstract_xml['#text']
            try:
                abstract_label = abstract_xml['@Label']
                abstract_paragraphs.append("{}: {}"
                    .format(abstract_label, abstract_text))
            except:
                abstract_paragraphs.append(abstract_text)

        elif isinstance(abstract_xml, list):
            for abstract_section in abstract_xml:
                try:
                    abstract_text = abstract_section['#text']
                except:
                    abstract_text = abstract_section

                try:
                    abstract_label = abstract_section['@Label']
                    abstract_paragraphs.append("{}: {}"
                        .format(abstract_label, abstract_text))
                except:
                    abstract_paragraphs.append(abstract_text)

        else:
            raise RuntimeError("Error parsing abstract.")

        return "\n\n".join(abstract_paragraphs)

    def set_abstract(self):
        """If record has an abstract, get it with PubMed ID"""
        if self.record['HasAbstract'] == 1:
            url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/' \
                  'efetch.fcgi?db=pubmed&rettype=abstract&id={}' \
                  .format(self.pmid)

            try:
                response = urlopen(url)
            except:
                self.abstract = ''
            else:
                xml = response.read().decode()
                self.abstract = self.parse_abstract(xml)

        else:
            self.abstract = ''

    def set_article_url(self):
        """
        If record has a DOI, set article URL based on where the DOI points.
        """
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
    (e.g., '22331878' or 'http://www.ncbi.nlm.nih.gov/pubmed/22331878')
    """

    def __init__(self, query, user_email):
        """
        Upon init: set email as required by API, determine whether query
        is PubMed ID or PubMed URL and retrieve PubMed record accordingly.
        """
        Entrez.email = user_email

        pmid_pattern = r'^\d+$'
        pmurl_pattern = r'^https?://www\.ncbi\.nlm\.nih\.gov/pubmed/\d+$'
        if re.match(pmid_pattern, query):
            pmid = query
        elif re.match(pmurl_pattern, query):
            pmid = self.parse_pubmed_url(query)
        else:
            raise RuntimeError(
                "Query ({}) doesn't appear to be a PubMed ID or PubMed URL"
                .format(query))

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

    # Example of PubMedLookup
    url = 'http://www.ncbi.nlm.nih.gov/pubmed/22331878'
    lookup = PubMedLookup(url, email)

    # Demo contents of entire record
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(lookup.record)

    # Example of Publication
    publication = Publication(lookup)
    print(
        """
TITLE:\n{title}\n
AUTHORS:\n{authors}\n
JOURNAL:\n{journal}\n
YEAR:\n{year}\n
URL:\n{url}\n
PUBMED:\n{pubmed}\n
CITATION:\n{citation}\n
ABSTRACT:\n{abstract}\n
        """
        .format(**{
            'title': publication.title,
            'authors': publication.authors,
            'journal': publication.journal,
            'year': publication.pub_year,
            'url': publication.url,
            'pubmed': publication.pubmed_url,
            'citation': publication.cite(),
            'abstract': publication.abstract,
        }))
