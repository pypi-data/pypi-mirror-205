#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# Author:  Bryce Harrington <bryce@canonical.com>
#
# Copyright (C) 2022 Bryce W. Harrington
#
# Released under GNU GPLv2 or later, read the file 'LICENSE.GPLv2+' for
# more information.

"""Trigger class tests"""

import os
import sys

import pytest

sys.path.insert(0, os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")))

from ppa.trigger import Trigger


def test_object():
    """Checks that Trigger objects can be instantiated."""
    trigger = Trigger('a', 'b', 'c', 'd', 'e')
    assert trigger


@pytest.mark.parametrize('pkg, ver, arch, series, ppa, testpkg, expected_repr', [
    ('a', 'b', 'c', 'd', 'e', 'f',
     "Trigger(package='a', version='b', arch='c', series='d', ppa='e', test_package='f')"),
    ('a', 'b', 'c', 'd', 'e', None,
     "Trigger(package='a', version='b', arch='c', series='d', ppa='e', test_package='a')"),
])
def test_repr(pkg, ver, arch, series, ppa, testpkg, expected_repr):
    """Checks Trigger object representation."""
    trigger = Trigger(pkg, ver, arch, series, ppa, testpkg)
    assert repr(trigger) == expected_repr


def test_str():
    """Checks Trigger object textual presentation."""
    trigger = Trigger('a', 'b', 'c', 'd', 'e')
    assert f"{trigger}" == 'a/b'

    trigger = Trigger('dovecot', '1:2.3.19.1+dfsg1-2ubuntu2', 'i386', 'kinetic', None)
    assert f"{trigger}" == 'dovecot/1:2.3.19.1+dfsg1-2ubuntu2'


@pytest.mark.parametrize('trigger, expected', [
    (
        Trigger('a', 'b', 'c', 'd', 'e'),
        "/packages/a/a/d/c"
    ), (
        Trigger('apache2', '2.4', 'amd64', 'kinetic', None),
        "/packages/a/apache2/kinetic/amd64"
    ), (
        Trigger('libwebsockets', '4.1.6-3', 'armhf', 'jammy', None),
        "/packages/libw/libwebsockets/jammy/armhf"
    )
])
def test_history_url(trigger, expected):
    """Checks that Trigger objects generate valid autopkgtest history urls"""
    assert expected in trigger.history_url


@pytest.mark.parametrize('trigger, expected', [
    (
        Trigger('a', 'b', 'c', 'd', 'e'),
        "/request.cgi?release=d&package=a&arch=c&trigger=a%2Fb&ppa=e"
    ), (
        Trigger('a', '1.2+git345', 'c', 'd', None),
        "/request.cgi?release=d&package=a&arch=c&trigger=a%2F1.2%2Bgit345"
    ), (
        Trigger('apache2', '2.4', 'amd64', 'kinetic', None),
        "/request.cgi?release=kinetic&package=apache2&arch=amd64&trigger=apache2%2F2.4"
    ), (
        Trigger('nut', '2.7.4-1', 'armhf', 'jammy', None),
        "/request.cgi?release=jammy&package=nut&arch=armhf&trigger=nut%2F2.7.4-1"
    ), (
        Trigger('apache2', '2.4', 'amd64', 'kinetic', 'ppa:aaa/bbb'),
        "/request.cgi?release=kinetic&package=apache2&arch=amd64&trigger=apache2%2F2.4&ppa=ppa%3Aaaa%2Fbbb"
    ), (
        Trigger('apache2', '2.4', 'amd64', 'kinetic', 'ppa:aaa/bbb', 'cinder'),
        "/request.cgi?release=kinetic&package=cinder&arch=amd64&trigger=apache2%2F2.4&ppa=ppa%3Aaaa%2Fbbb"
    )
])
def test_action_url(trigger, expected):
    """Checks that Trigger objects generate valid autopkgtest action urls"""
    assert expected in trigger.action_url
