#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# Author:  Bryce Harrington <bryce@canonical.com>
#
# Copyright (C) 2022 Bryce W. Harrington
#
# Released under GNU GPLv2 or later, read the file 'LICENSE.GPLv2+' for
# more information.

"""Subtest class tests"""

import os
import sys

import pytest

sys.path.insert(0, os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")))

from ppa.subtest import Subtest


def test_object():
    """Checks that Subtest objects can be instantiated."""
    subtest = Subtest('a UNKNOWN')
    # TODO: If no ':' in description, should throw exception?
    # TODO: Or add a function that parses lines and returns subtests?
    assert subtest


def test_repr():
    """Checks Subtest object representation."""
    subtest = Subtest('a PASS')
    assert repr(subtest) == "Subtest(line='a PASS')"


def test_str():
    """Checks Subtest object textual presentation."""
    subtest = Subtest('a PASS')
    assert 'PASS' in f"{subtest}"
    assert 'a' in f"{subtest}"
    assert '🟩' in f"{subtest}"


def test_desc():
    """Checks Subtest description is parsed correctly."""
    subtest = Subtest('a PASS')
    assert subtest.desc == 'a'

    subtest = Subtest('a FAIL descriptive text')
    assert subtest.desc == 'a'

    subtest = Subtest('a:b  PASS')
    assert subtest.desc == 'a:b'


@pytest.mark.parametrize('line, status', [
    ('a PASS', 'PASS'),
    ('b SKIP', 'SKIP'),
    ('c FAIL', 'FAIL'),
    ('d FAIL non-zero exit status 123', 'FAIL'),
    ('librust-clang-sys-dev:clang_10_0 FAIL non-zero exit status 101', 'FAIL'),
    ('f BAD', 'BAD'),
    ('g UNKNOWN', 'UNKNOWN'),
    ('h invalid', 'UNKNOWN'),
    ('i bAd', 'UNKNOWN'),
])
def test_status(line, status):
    """Checks Subtest status is parsed correctly."""
    subtest = Subtest(line)
    assert subtest.status == status

    subtest = Subtest('a PASS')


@pytest.mark.parametrize('line, icon', [
    ('a PASS', "🟩"),
    ('b SKIP', "🟧"),
    ('c FAIL', "🟥"),
    ('d BAD', "⛔"),
    ('e UNKNOWN', "⚪"),
    ('f invalid', "⚪"),
    ('f bAd', "⚪"),
])
def test_status_icon(line, icon):
    """Checks Subtest provides correct icon for status.

    :param str line: Subtest status line to be parsed.
    :param str icon: Resulting status icon that should be returned.
    """
    subtest = Subtest(line)
    assert subtest.status_icon == icon
