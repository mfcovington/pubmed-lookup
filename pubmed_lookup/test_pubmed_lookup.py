import copy
import unittest

from pubmed_lookup import Publication, PubMedLookup


class TestPublication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Get publication record
        email = ''
        cls.pmid = '22331878'
        lookup = PubMedLookup(cls.pmid, email)
        cls.record = Publication(lookup)

        # Set frequently used expected results
        cls.authors = 'Goodspeed D, Chehab EW, Min-Venditti A, Braam J, ' \
            'Covington MF'
        cls.issue = '12'
        cls.journal = 'Proc Natl Acad Sci U S A'
        cls.pages = '4674-7'
        cls.title = 'Arabidopsis synchronizes jasmonate-mediated defense ' \
            'with insect circadian behavior.'
        cls.volume = '109'
        cls.year = '2012'
        cls.citation_data = {
            'authors': cls.authors,
            'year': cls.year,
            'title': cls.title,
            'journal': cls.journal,
            'volume': cls.volume,
            'issue': cls.issue,
            'pages': cls.pages,
        }
        cls.base_citation = '{authors} ({year}). {title} {journal}'.format(
            **cls.citation_data)

    def test_fields(self):
        self.assertEqual(self.record.pmid, self.pmid)
        self.assertEqual(self.record.pubmed_url,
            'http://www.ncbi.nlm.nih.gov/pubmed/22331878')
        self.assertEqual(self.record.url,
            'http://www.pnas.org/content/109/12/4674')
        self.assertEqual(self.record.title, self.title)
        self.assertEqual(self.record.authors, self.authors)
        self.assertEqual(self.record.first_author, 'Goodspeed D')
        self.assertEqual(self.record.last_author, 'Covington MF')
        self.assertEqual(self.record.journal, self.journal)
        self.assertEqual(self.record.volume, self.volume)
        self.assertEqual(self.record.year, self.year)
        self.assertEqual(self.record.month, 3)
        self.assertEqual(self.record.day, '20')
        self.assertEqual(self.record.issue, self.issue)
        self.assertEqual(self.record.pages, self.pages)
        self.assertEqual(len(self.record.abstract), 1604)

    def test_authors_et_al(self):
        self.assertEqual(self.record.authors_et_al(), self.authors)
        self.assertEqual(self.record.authors_et_al(max_authors=3),
            'Goodspeed D, Chehab EW, Min-Venditti A, et al.')
        self.assertEqual(self.record.authors_et_al(max_authors=10),
            self.authors)

    def test_cite_mini(self):
        self.assertEqual(self.record.cite_mini(),
            'Goodspeed D - Covington MF - 2012 - Proc Natl Acad Sci U S A')

    def test_cite(self):
        self.assertEqual(self.record.cite(),
            '{} {volume}({issue}): {pages}.'.format(self.base_citation,
                **self.citation_data))

    def test_cite_without_pages(self):
        record_copy = copy.copy(self.record)
        record_copy.pages = ''
        self.assertEqual(record_copy.cite(), '{} {volume}({issue}).'.format(
            self.base_citation, **self.citation_data))

    def test_cite_without_issue(self):
        record_copy = copy.copy(self.record)
        record_copy.issue = ''
        self.assertEqual(record_copy.cite(), '{} {volume}: {pages}.'.format(
            self.base_citation, **self.citation_data))

    def test_cite_without_issue_pages(self):
        record_copy = copy.copy(self.record)
        record_copy.issue = ''
        record_copy.pages = ''
        self.assertEqual(record_copy.cite(), '{} {volume}.'.format(
            self.base_citation, **self.citation_data))

    def test_cite_without_issue_volume(self):
        record_copy = copy.copy(self.record)
        record_copy.issue = ''
        record_copy.volume = ''
        self.assertEqual(record_copy.cite(), '{} {pages}.'.format(
            self.base_citation, **self.citation_data))

    def test_cite_without_issue_pages_volume(self):
        record_copy = copy.copy(self.record)
        record_copy.issue = ''
        record_copy.pages = ''
        record_copy.volume = ''
        self.assertEqual(record_copy.cite(), '{}.'.format(self.base_citation))

    def test_missing_doi(self):
        record_copy = copy.copy(self.record)
        del record_copy.record['DOI']
        record_copy.set_article_url()
        self.assertEqual(record_copy.url, '')

    def test_invalid_doi(self):
        record_copy = copy.copy(self.record)
        record_copy.record.update({'DOI': 'not a valid DOI'})
        record_copy.set_article_url()
        self.assertEqual(record_copy.url, '')


class TestPubMedLookup(unittest.TestCase):
    def setUp(self):
        self.email = ''
        self.pubmed_url = 'http://www.ncbi.nlm.nih.gov/pubmed/22331878'
        self.pmid = '22331878'

    def test_pmid_and_url_return_same_record(self):
        self.assertEqual(PubMedLookup(self.pmid, self.email).record,
            PubMedLookup(self.pubmed_url, self.email).record)

    def test_parse_pubmed_url(self):
        self.assertEqual(PubMedLookup.parse_pubmed_url(self.pubmed_url),
            self.pmid)

    def test_invalid_query(self):
        with self.assertRaises(RuntimeError):
            PubMedLookup('not a valid query', self.email)


if __name__ == '__main__':
    unittest.main()
