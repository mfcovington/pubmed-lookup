import copy
import os
import unittest
from io import StringIO

from pubmed_lookup import command_line, Publication, PubMedLookup


article_url = 'https://www.pnas.org/content/109/12/4674'
citation = (
    'Goodspeed D, Chehab EW, Min-Venditti A, Braam J, Covington MF (2012). '
    'Arabidopsis synchronizes jasmonate-mediated defense with insect '
    'circadian behavior. Proc Natl Acad Sci U S A 109(12): 4674-7.')
doi_url = 'http://dx.doi.org/10.1073/pnas.1116368109'
mini_citation = 'Goodspeed D - Covington MF - 2012 - Proc Natl Acad Sci U S A'
pmid = '22331878'


class TestConsole(unittest.TestCase):
    """Test command-line tools."""

    def setUp(self):
        self.out = StringIO()

    def test_pubmed_citation(self):
        command_line.pubmed_citation([pmid], out=self.out)
        output = self.out.getvalue()
        self.assertEqual(output, citation + '\n')

    def test_pubmed_citation_m(self):
        command_line.pubmed_citation(['-m', pmid], out=self.out)
        output = self.out.getvalue()
        self.assertEqual(output, mini_citation + '\n')

    def test_pubmed_citation_mini(self):
        command_line.pubmed_citation(['--mini', pmid], out=self.out)
        output = self.out.getvalue()
        self.assertEqual(output, mini_citation + '\n')

    def test_pubmed_url(self):
        command_line.pubmed_url([pmid], out=self.out)
        output = self.out.getvalue()
        self.assertEqual(output, article_url + '\n')

    def test_pubmed_url_d(self):
        command_line.pubmed_url(['-d', pmid], out=self.out)
        output = self.out.getvalue()
        self.assertEqual(output, doi_url + '\n')

    def test_pubmed_url_doi(self):
        command_line.pubmed_url(['--doi', pmid], out=self.out)
        output = self.out.getvalue()
        self.assertEqual(output, doi_url + '\n')


class TestPublication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Get publication record
        email = ''
        cls.pmid = pmid
        cls.lookup = PubMedLookup(cls.pmid, email)
        cls.master_record = Publication(cls.lookup)

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

    def setUp(self):
        self.record = copy.copy(self.master_record)

    def test_fields(self):
        self.assertEqual(self.record.pmid, self.pmid)
        self.assertEqual(
            self.record.pubmed_url,
            'http://www.ncbi.nlm.nih.gov/pubmed/{}'.format(pmid))
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
        self.assertEqual(
            self.record.authors_et_al(max_authors=3),
            'Goodspeed D, Chehab EW, Min-Venditti A, et al.')
        self.assertEqual(
            self.record.authors_et_al(max_authors=10), self.authors)

    def test_cite_mini(self):
        self.assertEqual(self.record.cite_mini(), mini_citation)

    def test_cite(self):
        self.assertEqual(
            self.record.cite(), '{} {volume}({issue}): {pages}.'.format(
                self.base_citation, **self.citation_data))

    def test_cite_without_pages(self):
        self.record.pages = ''
        self.assertEqual(self.record.cite(), '{} {volume}({issue}).'.format(
            self.base_citation, **self.citation_data))

    def test_cite_without_issue(self):
        self.record.issue = ''
        self.assertEqual(self.record.cite(), '{} {volume}: {pages}.'.format(
            self.base_citation, **self.citation_data))

    def test_cite_without_issue_pages(self):
        self.record.issue = ''
        self.record.pages = ''
        self.assertEqual(self.record.cite(), '{} {volume}.'.format(
            self.base_citation, **self.citation_data))

    def test_cite_without_issue_volume(self):
        self.record.issue = ''
        self.record.volume = ''
        self.assertEqual(self.record.cite(), '{} {pages}.'.format(
            self.base_citation, **self.citation_data))

    def test_cite_without_issue_pages_volume(self):
        self.record.issue = ''
        self.record.pages = ''
        self.record.volume = ''
        self.assertEqual(self.record.cite(), '{}.'.format(self.base_citation))

    @unittest.skipIf(
        "TRAVIS" in os.environ and os.environ["TRAVIS"] == 'true',
        "Skipping this test on Travis CI.")
    def test_doi(self):
        self.assertEqual(
            self.record.url, 'https://www.pnas.org/content/109/12/4674')

    def test_missing_doi(self):
        del self.record.record['DOI']
        self.record.set_article_url()
        self.assertEqual(self.record.url, '')

    def test_invalid_doi(self):
        self.record.record.update({'DOI': 'not a valid DOI'})
        self.record.set_article_url()
        self.assertEqual(self.record.url, 'http://dx.doi.org/not a valid DOI')

    def test_dont_resolve_doi(self):
        record = Publication(self.lookup, resolve_doi=False)
        self.assertEqual(
            record.url, doi_url)


class TestPubMedLookup(unittest.TestCase):
    def setUp(self):
        self.email = ''
        self.pubmed_url = 'http://www.ncbi.nlm.nih.gov/pubmed/{}'.format(pmid)
        self.pmid = pmid

    def test_pmid_and_url_return_same_record(self):
        self.assertEqual(
            PubMedLookup(self.pmid, self.email).record,
            PubMedLookup(self.pubmed_url, self.email).record)

    def test_parse_pubmed_url(self):
        self.assertEqual(
            PubMedLookup.parse_pubmed_url(self.pubmed_url), self.pmid)

    def test_invalid_query(self):
        with self.assertRaises(RuntimeError):
            PubMedLookup('not a valid query', self.email)


if __name__ == '__main__':
    unittest.main()
