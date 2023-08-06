#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# Author:  Bryce Harrington <bryce@canonical.com>
#
# Copyright (C) 2019 Bryce W. Harrington
#
# Released under GNU GPLv2 or later, read the file 'LICENSE.GPLv2+' for
# more information.

import os
import sys

import pytest

sys.path.insert(0, os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")))

from ppa.ppa import Ppa, ppa_address_split, get_ppa


def test_object():
    """Check that PPA objects can be instantiated."""
    ppa = Ppa('test-ppa-name', 'test-team-name')
    assert ppa


def test_description():
    """Check specifying a description when creating a PPA."""
    ppa = Ppa('test-ppa-name', 'test-team-name', 'test-description')

    assert 'test-description' in ppa.ppa_description


def test_address():
    """Check getting the PPA address."""
    ppa = Ppa('test', 'team')
    assert ppa.address == "ppa:team/test"


@pytest.mark.parametrize('address, default_team, expected', [
    # Successful cases
    ('bb', 'me', ('me', 'bb')),
    ('123', 'me', ('me', '123')),
    ('a/123', 'me', ('a', '123')),
    ('ppa:a/bb', None, ('a', 'bb')),
    ('ppa:ç/bb', None, ('ç', 'bb')),
    ('https://launchpad.net/~a/+archive/ubuntu/bb', None, ('a', 'bb')),

    # Expected failure cases
    ('ppa:', None, (None, None)),
    (None, None, (None, None)),
    ('', None, (None, None)),
    ('/', None, (None, None)),
    (':/', None, (None, None)),
    ('////', None, (None, None)),
    ('ppa:/', None, (None, None)),
    ('ppa:a/', None, (None, None)),
    ('ppa:/bb', None, (None, None)),
    ('ppa:a/bç', None, (None, None)),
    ('ppa:A/bb', None, (None, None)),
    ('ppa/a/bb', None, (None, None)),
    ('ppa:a/bb/c', None, (None, None)),
    ('ppa:a/bB', None, (None, None)),
    ('http://launchpad.net/~a/+archive/ubuntu/bb', None, (None, None)),
    ('https://example.com/~a/+archive/ubuntu/bb', None, (None, None)),
    ('https://launchpad.net/~a/+archive/nobuntu/bb', None, (None, None)),
])
def test_ppa_address_split(address, default_team, expected):
    """Check ppa address input strings can be parsed properly."""
    result = ppa_address_split(address, default_team=default_team)
    assert result == expected


def test_get_ppa():
    ppa = get_ppa(None, {'team_name': 'a', 'ppa_name': 'bb'})
    assert type(ppa) is Ppa
    assert ppa.team_name == 'a'
    assert ppa.ppa_name == 'bb'
