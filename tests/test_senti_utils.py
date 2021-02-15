#!/usr/bin/env python

"""Tests for `sentiment_timeseries` package."""

import pytest

import sentimenttime.senti_utils as senti_utils
# from sentimenttime.senti import say_hello


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_file2str_chars_len():
    assert len(senti_utils.file2str('./books/cdikens_christmascarol.txt')) == 161789

def test_file2str_lines_len():
    assert len(senti_utils.file2str('./books/cdikens_christmascarol.txt').split('\n')) == 23
    