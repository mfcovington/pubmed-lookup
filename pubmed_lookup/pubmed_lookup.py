import datetime
import re
from functools import reduce
from urllib.error import URLError
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
        title, authors, first_author, last_author, journal, volume, issue,
        pages, url, abstract, year, month, and day)
        """
        self.record = pubmed_record.record
        self.pmid = self.record.get('Id')
        self.pubmed_url = 'http://www.ncbi.nlm.nih.gov/pubmed/{}' \
                          .format(self.pmid)
        self.title = self.record.get('Title')
        self._author_list = self.record.get('AuthorList')
        self.authors = ", ".join(self._author_list)
        self.first_author = self._author_list[0]
        self.last_author = self._author_list[-1]
        self.journal = self.record.get('Source')
        self.volume = self.record.get('Volume')
        self.issue = self.record.get('Issue')
        self.pages = self.record.get('Pages')
        self.set_article_url()

        xml_dict = self.get_pubmed_xml()
        self.set_abstract(xml_dict)
        self.set_pub_year_month_day(xml_dict)

    def authors_et_al(self, max_authors=5):
        """
        Return string with a truncated author list followed by 'et al.'
        """
        author_list = self._author_list
        if len(author_list) <= max_authors:
            authors_et_al = self.authors
        else:
            authors_et_al = ", ".join(
                self._author_list[:max_authors]) + ", et al."
        return authors_et_al

    def cite(self, max_authors=5):
        """
        Return string with a citation for the record, formatted as:
        '{authors} ({year}). {title} {journal} {volume}({issue}): {pages}.'
        """
        citation_data = {
            'title': self.title,
            'authors': self.authors_et_al(max_authors),
            'year': self.year,
            'journal': self.journal,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
        }
        citation = "{authors} ({year}). {title} {journal}".format(
            **citation_data)

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

    def cite_mini(self):
        """
        Return string with a citation for the record, formatted as:
        '{first_author} - {year} - {journal}'
        """
        citation_data = [self.first_author]

        if len(self._author_list) > 1:
            citation_data.append(self.last_author)

        citation_data.extend([self.year, self.journal])

        return " - ".join(citation_data)

    @staticmethod
    def parse_abstract(xml_dict):
        """
        Parse PubMed XML dictionary to retrieve abstract.
        """
        key_path = ['PubmedArticleSet', 'PubmedArticle', 'MedlineCitation',
                    'Article', 'Abstract', 'AbstractText']
        abstract_xml = reduce(dict.get, key_path, xml_dict)

        abstract_paragraphs = []

        if isinstance(abstract_xml, str):
            abstract_paragraphs.append(abstract_xml)

        elif isinstance(abstract_xml, dict):
            abstract_text = abstract_xml.get('#text')
            try:
                abstract_label = abstract_xml['@Label']
            except KeyError:
                abstract_paragraphs.append(abstract_text)
            else:
                abstract_paragraphs.append(
                    "{}: {}".format(abstract_label, abstract_text))

        elif isinstance(abstract_xml, list):
            for abstract_section in abstract_xml:
                try:
                    abstract_text = abstract_section['#text']
                except KeyError:
                    abstract_text = abstract_section

                try:
                    abstract_label = abstract_section['@Label']
                except KeyError:
                    abstract_paragraphs.append(abstract_text)
                else:
                    abstract_paragraphs.append(
                        "{}: {}".format(abstract_label, abstract_text))

        else:
            raise RuntimeError("Error parsing abstract.")

        return "\n\n".join(abstract_paragraphs)

    def get_pubmed_xml(self):
        """
        Use a PubMed ID to retrieve PubMed metadata in XML form.
        """
        url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/' \
              'efetch.fcgi?db=pubmed&rettype=abstract&id={}' \
              .format(self.pmid)

        try:
            response = urlopen(url)
        except URLError:
            xml_dict = ''
        else:
            xml = response.read().decode()
            xml_dict = xmltodict.parse(xml)

        return xml_dict

    def set_abstract(self, xml_dict):
        """
        If record has an abstract, get it extract it from PubMed's XML data
        """
        if self.record.get('HasAbstract') == 1 and xml_dict:
            self.abstract = self.parse_abstract(xml_dict)
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
            except URLError:
                self.url = ''
            else:
                self.url = response.geturl()
        else:
            self.url = ''

    def set_pub_year_month_day(self, xml_dict):
        """
        Set publication year, month, day from PubMed's XML data
        """
        key_path = ['PubmedArticleSet', 'PubmedArticle', 'MedlineCitation',
                    'Article', 'Journal', 'JournalIssue', 'PubDate']
        pubdate_xml = reduce(dict.get, key_path, xml_dict)

        if isinstance(pubdate_xml, dict):
            self.year = pubdate_xml.get('Year')
            month_short = pubdate_xml.get('Month')
            self.day = pubdate_xml.get('Day')

            try:
                self.month = datetime.datetime.strptime(
                    month_short, "%b").month
            except ValueError:
                self.month = ''

        else:
            self.year = ''
            self.month = ''
            self.day = ''


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
        if re.match(pmid_pattern, str(query)):
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
        pattern = re.compile(r'^/pubmed/(\d+)$')
        pmid = pattern.match(parse_result.path).group(1)
        return pmid

    @staticmethod
    def get_pubmed_record(pmid):
        """Get PubMed record from PubMed ID."""
        handle = Entrez.esummary(db="pubmed", id=pmid)
        record = Entrez.read(handle)
        return record
