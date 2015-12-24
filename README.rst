*************
pubmed-lookup
*************


.. image:: https://badge.fury.io/py/pubmed-lookup.svg
    :target: http://badge.fury.io/py/pubmed-lookup
    :alt: PyPI Version

.. image:: https://travis-ci.org/mfcovington/pubmed-lookup.svg?branch=master
    :target: https://travis-ci.org/mfcovington/pubmed-lookup
    :alt: Build Status

.. image:: https://coveralls.io/repos/mfcovington/pubmed-lookup/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/mfcovington/pubmed-lookup?branch=master
    :alt: Test Coverage

.. image:: https://landscape.io/github/mfcovington/pubmed-lookup/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mfcovington/pubmed-lookup/master
   :alt: Code Health

``pubmed-lookup`` is a Python package to lookup PubMed records and make Publication objects with info about a scientific publication.

Source code is available on GitHub at `mfcovington/pubmed-lookup <https://github.com/mfcovington/pubmed-lookup>`_.

.. contents:: :local:


Installation
============

**PyPI**

.. code-block:: sh

    pip install pubmed-lookup

**GitHub (development branch)**

.. code-block:: sh

    pip install git+http://github.com/mfcovington/pubmed-lookup.git@develop


Usage
=====

- Retrieve a PubMed record:

.. code-block:: python

    from pubmed_lookup import PubMedLookup

    # NCBI will contact user by email if excessive queries are detected
    email = ''
    url = 'http://www.ncbi.nlm.nih.gov/pubmed/22331878'
    lookup = PubMedLookup(url, email)


- Create a Publication object:

.. code-block:: python

    from pubmed_lookup import Publication
    
    publication = Publication(lookup)


- Access the Publication object's attributes:

.. code-block:: python

    print(
    """
    TITLE:\n{title}\n
    AUTHORS:\n{authors}\n
    JOURNAL:\n{journal}\n
    YEAR:\n{year}\n
    MONTH:\n{month}\n
    DAY:\n{day}\n
    URL:\n{url}\n
    PUBMED:\n{pubmed}\n
    CITATION:\n{citation}\n
    MINICITATION:\n{mini_citation}\n
    ABSTRACT:\n{abstract}\n
    """
    .format(**{
        'title': publication.title,
        'authors': publication.authors,
        'journal': publication.journal,
        'year': publication.year,
        'month': publication.month,
        'day': publication.day,
        'url': publication.url,
        'pubmed': publication.pubmed_url,
        'citation': publication.cite(),
        'mini_citation': publication.cite_mini(),
        'abstract': repr(publication.abstract),
    }))


- Output of example:

    TITLE:
    Arabidopsis synchronizes jasmonate-mediated defense with insect circadian behavior.
    
    AUTHORS:
    Goodspeed D, Chehab EW, Min-Venditti A, Braam J, Covington MF
    
    JOURNAL:
    Proc Natl Acad Sci U S A
    
    YEAR:
    2012
    
    MONTH:
    3
    
    DAY:
    20
    
    URL:
    http://www.pnas.org/content/109/12/4674
    
    PUBMED:
    http://www.ncbi.nlm.nih.gov/pubmed/22331878
    
    CITATION:
    Goodspeed D, Chehab EW, Min-Venditti A, Braam J, Covington MF (2012). Arabidopsis synchronizes jasmonate-mediated defense with insect circadian behavior. Proc Natl Acad Sci U S A 109(12): 4674-7.
    
    MINICITATION:
    Goodspeed D - Covington MF - 2012 - Proc Natl Acad Sci U S A
    
    ABSTRACT:
    Diverse life forms have evolved internal clocks enabling them to monitor time and thereby anticipate the daily environmental changes caused by Earth's rotation. The plant circadian clock regulates expression of about one-third of the Arabidopsis genome, yet the physiological relevance of this regulation is not fully understood. Here we show that the circadian clock, acting with hormone signals, provides selective advantage to plants through anticipation of and enhanced defense against herbivory. We found that cabbage loopers (Trichoplusia ni) display rhythmic feeding behavior that is sustained under constant conditions, and plants entrained in light/dark cycles coincident with the entrainment of the T. ni suffer only moderate tissue loss due to herbivory. In contrast, plants entrained out-of-phase relative to the insects are significantly more susceptible to attack. The in-phase entrainment advantage is lost in plants with arrhythmic clocks or deficient in jasmonate hormone; thus, both the circadian clock and jasmonates are required. Circadian jasmonate accumulation occurs in a phase pattern consistent with preparation for the onset of peak circadian insect feeding behavior, providing evidence for the underlying mechanism of clock-enhanced herbivory resistance. Furthermore, we find that salicylate, a hormone involved in biotrophic defense that often acts antagonistically to jasmonates, accumulates in opposite phase to jasmonates. Our results demonstrate that the plant circadian clock provides a strong physiological advantage by performing a critical role in Arabidopsis defense."

*Version 0.1.4*
