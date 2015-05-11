# http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec136
# pip install biopython

import sys
import re
from urllib.parse import urlparse
from urllib.request import urlopen
from Bio import Entrez


# pubmed_url = 'http://www.ncbi.nlm.nih.gov/pubmed/25122667'
pubmed_url = sys.argv[1]
parse_result = urlparse(pubmed_url)
# parse_result.path

pattern = re.compile('^/pubmed/(\d+)$')

pmid = pattern.match(parse_result.path).group(1)



# pmid = 25122667
Entrez.email = 'mfcovington@gmail.com'

handle = Entrez.esummary(db="pubmed", id=pmid)
record = Entrez.read(handle)
# record[0]

title = record[0]['Title']
# record[0]['AuthorList']
author_string = ", ".join(record[0]['AuthorList'])

journal = record[0]['Source']
pub_date = record[0]['PubDate']



# record[0]['DOI']

# DOI:
# http://dx.doi.org/XXXX
# http://dx.doi.org/10.1534/g3.114.012526

doi_url = "/".join(['http://dx.doi.org', record[0]['DOI']])

# try:
#     response = urlopen(doi_url)
# except:
#     article_url = ''
# else:
#     article_url = response.geturl()

# resp.getcode()

# doi_url for http://www.ncbi.nlm.nih.gov/pubmed/17589502 -- HTTPError: HTTP Error 401: Unauthorized




print(title)
print(author_string)
print(journal)
print(pub_date)
# print(article_url)
print(doi_url)
print(pubmed_url)





##########################
##########################
##########################
##########################
##########################

# handle = Entrez.efetch(db='pubmed', id=str(pmid))
# print(handle.read())

# handle = Entrez.efetch(db='pubmed', id=str(pmid), retmode='xml')
# record = Entrez.read(handle)
# handle.close()
# abstract_text = str(record[0]['MedlineCitation']['Article']['Abstract']['AbstractText'][0])




# 'EPubDate': '2014 Aug 12'
# 'Item': []
# 'ESSN': '2160-1836'
# 'ELocationID': 'pii: g3.114.012526. doi: 10.1534/g3.114.012526'
# 'FullJournalName': 'G3 (Bethesda, Md.)'
# 'HasAbstract': 1
# 'DOI': '10.1534/g3.114.012526'
# 'AuthorList': ['Devisetty UK', 'Covington MF', 'Tat AV', 'Lekkala S', 'Maloof JN']
# 'Pages': ''
# 'NlmUniqueID': '101566598'
# 'ArticleIds':
# 'pubmed': ['25122667']
# 'medline': []
# 'pii': 'g3.114.012526'
# 'doi': '10.1534/g3.114.012526'
# 'rid': '25122667'
# 'eid': '25122667'}
# 'LangList': ['English']
# 'Volume': ''
# 'PubDate': '2014 Aug 12'
# 'References': []
# 'PubTypeList': ['Journal Article']
# 'LastAuthor': 'Maloof JN'
# 'Id': '25122667'
# 'Title': 'Polymorphism Identification and Improved Genome Annotation of Brassica rapa through Deep RNA Sequencing.'
# 'PubStatus': 'aheadofprint'
# 'SO': '2014 Aug 12;'
# 'Source': 'G3 (Bethesda)'
# 'History':
# 'pubmed': ['2014/08/15 06:00']
# 'medline': ['2014/08/15 06:00']
# 'entrez': '2014/08/15 06:00'}
# 'Issue': ''
# 'ISSN': ''
# 'PmcRefCount': 0
# 'RecordStatus': 'PubMed - as supplied by publisher'}



