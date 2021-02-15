#!/usr/bin/env python

"""Tests for `sentiment_timeseries` package."""

import pytest


from sentimenttime.hello import say_hello


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

def test_helloword_no_params():
    assert say_hello() == "Hello, World!"
    
def test_hello_with_params():
    assert say_hello("Everyone") == "Hello, Everyone!"