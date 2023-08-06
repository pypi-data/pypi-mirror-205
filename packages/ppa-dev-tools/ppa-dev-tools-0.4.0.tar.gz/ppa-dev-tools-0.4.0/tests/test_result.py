#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# Author:  Bryce Harrington <bryce@canonical.com>
#
# Copyright (C) 2022 Bryce W. Harrington
#
# Released under GNU GPLv2 or later, read the file 'LICENSE.GPLv2+' for
# more information.

"""Results class tests"""

import os
import sys
import time

import gzip

sys.path.insert(0, os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")))
DATA_DIR = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "data"))

from ppa.result import Result


def test_object():
    """Checks that Result objects can be instantiated."""
    result = Result('url', None, 'b', 'c', 'd')
    assert result


def test_repr():
    """Checks Result object representation."""
    result = Result('url', None, 'b', 'c', 'd')
    # TODO: Should this include the full set of args?
    assert repr(result) == "Result(url='url')"


def test_str():
    """Checks Result object textual presentation."""
    timestamp = time.strptime('20030201_040506', "%Y%m%d_%H%M%S")
    result = Result('url', timestamp, 'b', 'c', 'd')
    assert f"{result}" == 'd on b for c       @ 01.02.03 04:05:06'


def test_timestamp():
    """Checks Result object formats the result's time correctly."""
    timestamp = time.strptime('20030201_040506', "%Y%m%d_%H%M%S")
    result = Result('url', timestamp, 'b', 'c', 'd')
    assert f"{result.timestamp}" == '01.02.03 04:05:06'


def test_log(tmp_path):
    """Checks that the log content of a Result is available."""
    f = tmp_path / "result.log.gz"
    compressed_text = gzip.compress(bytes('abcde', 'utf-8'))
    f.write_bytes(compressed_text)

    result = Result(f"file://{f}", None, None, None, None)
    assert result.log == "abcde"


def test_triggers():
    """Checks that autopkgtest triggers can be extracted from test result logs."""
    result = Result(f"file://{DATA_DIR}/results-six-s390x.log.gz", None, None, None, None)
    assert result.triggers == ['pygobject/3.42.2-2', 'six/1.16.0-4']
