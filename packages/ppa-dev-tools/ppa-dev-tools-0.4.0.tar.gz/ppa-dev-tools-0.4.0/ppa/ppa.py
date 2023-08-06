#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# Author:  Bryce Harrington <bryce@canonical.com>
#
# Copyright (C) 2019 Bryce W. Harrington
#
# Released under GNU GPLv2 or later, read the file 'LICENSE.GPLv2+' for
# more information.

"""A wrapper around a Launchpad Personal Package Archive object."""

import re
import sys

from functools import lru_cache
from lazr.restfulclient.errors import BadRequest, NotFound, Unauthorized

from .constants import URL_AUTOPKGTEST
from .io import open_url
from .job import (get_waiting, get_running)


class PpaDoesNotExist(BaseException):
    """Exception indicating a requested PPA could not be found."""

    def __init__(self, ppa_name, team_name, message=None):
        """Initializes the exception object.

        :param str ppa_name: The name of the missing PPA.
        :param str message: An error message.
        """
        self.ppa_name = ppa_name
        self.team_name = team_name
        self.message = message

    def __str__(self):
        """Printable error message.

        :rtype str:
        :return: Error message about the failure.
        """
        if self.message:
            return self.message
        return f"The PPA '{self.ppa_name}' does not exist for team or user '{self.team_name}'"


class Ppa:
    """Encapsulates data needed to access and conveniently wrap a PPA.

    This object proxies a PPA, allowing lazy initialization and caching
    of data from the remote.
    """
    def __init__(self, ppa_name, team_name, ppa_description=None, service=None):
        """Initializes a new Ppa object for a given PPA.

        This creates only the local representation of the PPA, it does
        not cause a new PPA to be created in Launchpad.  For that, see
        PpaGroup.create()

        :param str ppa_name: The name of the PPA within the team's namespace.
        :param str team_name: The name of the team or user that owns the PPA.
        :param str ppa_description: Optional description text for the PPA.
        :param launchpadlib.service service: The Launchpad service object.
        """
        if not ppa_name:
            raise ValueError("undefined ppa_name.")
        if not team_name:
            raise ValueError("undefined team_name.")

        self.ppa_name = ppa_name
        self.team_name = team_name
        if ppa_description is None:
            self.ppa_description = ''
        else:
            self.ppa_description = ppa_description
        self._service = service

    def __repr__(self) -> str:
        """Machine-parsable unique representation of object.

        :rtype: str
        :returns: Official string representation of the object.
        """
        return (f'{self.__class__.__name__}('
                f'ppa_name={self.ppa_name!r}, team_name={self.team_name!r})')

    def __str__(self) -> str:
        """Returns a displayable string identifying the PPA.

        :rtype: str
        :returns: Displayable representation of the PPA.
        """
        return f"{self.team_name}/{self.name}"

    @property
    @lru_cache
    def archive(self):
        """Retrieves the LP Archive object from the Launchpad service.

        :rtype: archive
        :returns: The Launchpad archive object.
        :raises PpaDoesNotExist: Raised if a PPA does not exist in Launchpad.
        """
        if not self._service:
            raise AttributeError("Ppa object not connected to the Launchpad service")
        try:
            owner = self._service.people[self.team_name]
            return owner.getPPAByName(name=self.ppa_name)
        except NotFound:
            raise PpaDoesNotExist(self.ppa_name, self.team_name)

    @lru_cache
    def exists(self) -> bool:
        """Returns true if the PPA exists in Launchpad."""
        try:
            self.archive
            return True
        except PpaDoesNotExist:
            return False

    @property
    @lru_cache
    def address(self):
        """The proper identifier of the PPA.

        :rtype: str
        :returns: The full identification string for the PPA.
        """
        return "ppa:{}/{}".format(self.team_name, self.ppa_name)

    @property
    def name(self):
        """The name portion of the PPA's address.

        :rtype: str
        :returns: The name of the PPA.
        """
        return self.ppa_name

    @property
    def url(self):
        """The HTTP url for the PPA in Launchpad.

        :rtype: str
        :returns: The url of the PPA.
        """
        return self.archive.web_link

    @property
    def description(self):
        """The description body for the PPA.

        :rtype: str
        :returns: The description body for the PPA.
        """
        return self.ppa_description

    def set_description(self, description):
        """Configures the displayed description for the PPA.

        :rtype: bool
        :returns: True if successfully set description, False on error.
        """
        self.ppa_description = description
        try:
            a = self.archive
        except PpaDoesNotExist as e:
            print(e)
            return False
        a.description = description
        retval = a.lp_save()
        print("setting desc to '{}'".format(description))
        print("desc is now '{}'".format(self.archive.description))
        return retval and self.archive.description == description

    @property
    @lru_cache
    def publish(self):
        return self.archive.publish

    def set_publish(self, publish: bool):
        if publish is None:
            return
        self.archive.publish = publish
        self.archive.lp_save()

    @property
    @lru_cache
    def architectures(self) -> list[str]:
        """Returns the architectures configured to build packages in the PPA.

        :rtype: list[str]
        :returns: List of architecture names, or None on error.
        """
        try:
            return [proc.name for proc in self.archive.processors]
        except PpaDoesNotExist as e:
            sys.stderr.write(e)
            return None

    def set_architectures(self, architectures: list[str]) -> bool:
        """Configures the architectures used to build packages in the PPA.

        Note that some architectures may only be available upon request
        from Launchpad administrators.  ppa.constants.ARCHES_PPA is a
        list of standard architectures that don't require permissions.

        :param list[str] architectures: List of processor architecture names
        :rtype: bool
        :returns: True if architectures could be set, False on error or
            if no architectures were specified.
        """
        if not architectures:
            return False
        base = self._service.API_ROOT_URL.rstrip('/')
        procs = []
        for arch in architectures:
            procs.append(f'{base}/+processors/{arch}')
        try:
            self.archive.setProcessors(processors=procs)
            return True
        except PpaDoesNotExist as e:
            sys.stderr.write(e)
            return False

    @property
    @lru_cache
    def dependencies(self) -> list[str]:
        """Returns the additional PPAs configured for building packages in this PPA.

        :rtype: list[str]
        :returns: List of PPA addresses
        """
        ppa_addresses = []
        for dep in self.archive.dependencies:
            ppa_dep = dep.dependency
            ppa_addresses.append(ppa_dep.reference)
        return ppa_addresses

    def set_dependencies(self, ppa_addresses: list[str]):
        """Configures the additional PPAs used to build packages in this PPA.

        This removes any existing PPA dependencies and adds the ones
        in the corresponding list.  If any of these new PPAs cannot be
        found, this routine bails out without changing the current set.

        :param list[str] ppa_addresses: Additional PPAs to add
        """
        base = self._service.API_ROOT_URL.rstrip('/')
        new_ppa_deps = []
        for ppa_address in ppa_addresses:
            team_name, ppa_name = ppa_address_split(ppa_address)
            new_ppa_dep = f'{base}/~{team_name}/+archive/ubuntu/{ppa_name}'
            new_ppa_deps.append(new_ppa_dep)

        # TODO: Remove all existing dependencies
#        for ppa_dep in self.archive.dependencies:
#            the_ppa.removeArchiveDependency(ppa_dep)

        # TODO: Not sure what to pass here, maybe a string ala 'main'?
        component = None

        # TODO: Allow setting alternate pockets
        # TODO: Maybe for convenience it should be same as what's set for main archive?
        pocket = 'Release'

        for ppa_dep in new_ppa_deps:
            self.archive.addArchiveDependency(
                component=component,
                dependency=ppa_dep,
                pocket=pocket)
        # TODO: Error checking
        #       This can throw ArchiveDependencyError if the ppa_address does not fit the_ppa

    def get_binaries(self, distro=None, series=None, arch=None):
        """Retrieves the binary packages available in the PPA.

        :param distribution distro: The Launchpad distribution object.
        :param str series: The distro's codename for the series.
        :param str arch: The hardware architecture.
        :rtype: list[binary_package_publishing_history]
        :returns: List of binaries, or None on error
        """
        if distro is None and series is None and arch is None:
            try:
                return self.archive.getPublishedBinaries()
            except PpaDoesNotExist as e:
                print(e)
                return None
        # elif series:
        #     das = get_das(distro, series, arch)
        #     ds = distro.getSeries(name_or_version=series)
        print("Unimplemented")
        return []

    def get_source_publications(self, distro=None, series=None, arch=None):
        """Retrieves the source packages in the PPA.

        :param distribution distro: The Launchpad distribution object.
        :param str series: The distro codename for the series.
        :param str arch: The hardware architecture.

        :rtype: iterator
        :returns: Collection of source publications, or None on error
        """
        if distro and series and arch:
            # das = get_das(distro, series, arch)
            # ds = distro.getSeries(name_or_version=series)
            print("Unimplemented")
            return None

        try:
            for source_publication in self.archive.getPublishedSources():
                if source_publication.status not in ('Superseded', 'Deleted', 'Obsolete'):
                    yield source_publication
        except PpaDoesNotExist as e:
            print(e)
            return None

        return None

    def destroy(self):
        """Deletes the PPA.

        :rtype: bool
        :returns: True if PPA was successfully deleted, is in process of
            being deleted, no longer exists, or didn't exist to begin with.
            False if the PPA could not be deleted for some reason and is
            still existing.
        """
        try:
            return self.archive.lp_delete()
        except PpaDoesNotExist as e:
            print(e)
            return True
        except BadRequest:
            # Will report 'Archive already deleted' if deleted but not yet gone
            # we can treat this as successfully destroyed
            return True

    def has_packages(self):
        """Checks if the PPA has any source packages.

        :rtype: bool
        :returns: True if PPA contains packages, False if empty or doesn't exit.
        """
        return list(self.archive.getPublishedSources()) != []

    def has_pending_publications(self):
        pending_publication_sources = {}
        required_builds = {}
        pending_publication_builds = {}
        published_builds = {}

        for source_publication in self.get_source_publications():
            if not source_publication.date_published:
                pending_publication_sources[source_publication.self_link] = source_publication

            # iterate over the getBuilds result with no status restriction to get build records
            for build in source_publication.getBuilds():
                required_builds[build.self_link] = build

        for binary_publication in self.get_binaries():
            # Ignore failed builds
            build = binary_publication.build
            if build.buildstate != "Successfully built":
                continue

            # Skip binaries for obsolete sources
            source_publication = build.current_source_publication
            if source_publication is None:
                continue
            elif (source_publication.status in ('Superseded', 'Deleted', 'Obsolete')):
                continue

            if binary_publication.status == "Pending":
                pending_publication_builds[binary_publication.build_link] = binary_publication
            elif binary_publication.status == "Published":
                published_builds[binary_publication.build_link] = binary_publication

        retval = False
        num_builds_waiting = (
            len(required_builds) - len(pending_publication_builds) - len(published_builds)
        )
        if num_builds_waiting != 0:
            num_build_failures = 0
            builds_waiting_output = ''
            builds_failed_output = ''
            for build in required_builds.values():
                if build.buildstate == "Successfully built":
                    continue
                elif build.buildstate == "Failed to build":
                    num_build_failures += 1
                    builds_failed_output += "  - {} ({}) {}: {}\n".format(
                        build.source_package_name,
                        build.source_package_version,
                        build.arch_tag,
                        build.buildstate)
                else:
                    builds_waiting_output += "  - {} ({}) {}: {}\n".format(
                        build.source_package_name,
                        build.source_package_version,
                        build.arch_tag,
                        build.buildstate)
            if num_builds_waiting <= num_build_failures:
                print("* Some builds have failed:")
                print(builds_failed_output)
            elif builds_waiting_output != '':
                print("* Still waiting on these builds:")
                print(builds_waiting_output)
            retval = True

        if len(pending_publication_builds) != 0:
            num = len(pending_publication_builds)
            print(f"* Still waiting on {num} build publications:")
            for pub in pending_publication_builds.values():
                print("  - {}".format(pub.display_name))
            retval = True
        if len(pending_publication_sources) != 0:
            num = len(pending_publication_sources)
            print(f"* Still waiting on {num} source publications:")
            for pub in pending_publication_sources.values():
                print("  - {}".format(pub.display_name))
            retval = True
        if ((list(required_builds.keys()).sort() != list(published_builds.keys()).sort())):
            print("* Missing some builds")
            retval = True

        if not retval:
            print("Successfully published all builds for all architectures")
        return retval

    def get_autopkgtest_waiting(self, releases):
        """Returns iterator of queued autopkgtests for this PPA.

        See get_waiting() for details

        :param list[str] releases: The Ubuntu series codename(s), or None.
        :rtype: Iterator[Job]
        :returns: Currently waiting jobs, if any, or an empty list on error
        """
        response = open_url(f"{URL_AUTOPKGTEST}/queues.json", "waiting autopkgtests")
        if response:
            return get_waiting(response, releases=releases, ppa=str(self))
        return []

    def get_autopkgtest_running(self, releases):
        """Returns iterator of queued autopkgtests for this PPA.

        See get_running() for details

        :param list[str] releases: The Ubuntu series codename(s), or None.
        :rtype: Iterator[Job]
        :returns: Currently running jobs, if any, or an empty list on error
        """
        response = open_url(f"{URL_AUTOPKGTEST}/static/running.json", "running autopkgtests")
        if response:
            return get_running(response, releases=releases, ppa=str(self))
        return []


def ppa_address_split(ppa_address, default_team=None):
    """Parse an address for a PPA into its team and name components.

    :param str ppa_address: A ppa name or address.
    :param str default_team: (Optional) name of team to use if missing.
    :rtype: tuple(str, str)
    :returns: The team name and ppa name as a tuple, or (None, None) on error.
    """
    if not ppa_address or len(ppa_address) < 2:
        return (None, None)
    if ppa_address.startswith('ppa:'):
        if '/' not in ppa_address:
            return (None, None)
        rem = ppa_address.split('ppa:', 1)[1]
        team_name = rem.split('/', 1)[0]
        ppa_name = rem.split('/', 1)[1]
    elif ppa_address.startswith('http'):
        # Only launchpad PPA urls are supported
        m = re.search(r'https:\/\/launchpad\.net\/~([^/]+)\/\+archive\/ubuntu\/(.+)$', ppa_address)
        if not m:
            return (None, None)
        team_name = m.group(1)
        ppa_name = m.group(2)
    elif '/' in ppa_address:
        team_name = ppa_address.split('/', 1)[0]
        ppa_name = ppa_address.split('/', 1)[1]
    else:
        team_name = default_team
        ppa_name = ppa_address

    if (team_name
        and ppa_name
        and not (any(x.isupper() for x in team_name))
        and not (any(x.isupper() for x in ppa_name))
        and ppa_name.isascii()
        and '/' not in ppa_name
        and len(ppa_name) > 1):
        return (team_name, ppa_name)

    return (None, None)


def get_das(distro, series_name, arch_name):
    """Retrieves the arch-series for the given distro.

    :param distribution distro: The Launchpad distribution object.
    :param str series_name: The distro's codename for the series.
    :param str arch_name: The hardware architecture.
    :rtype: distro_arch_series
    :returns: A Launchpad distro_arch_series object, or None on error.
    """
    if series_name is None or series_name == '':
        return None

    for series in distro.series:
        if series.name != series_name:
            continue
        return series.getDistroArchSeries(archtag=arch_name)
    return None


def get_ppa(lp, config):
    """Load the specified PPA from Launchpad.

    :param Lp lp: The Launchpad wrapper object.
    :param dict config: Configuration param:value map.
    :rtype: Ppa
    :returns: Specified PPA as a Ppa object.
    """
    return Ppa(
        ppa_name=config.get('ppa_name', None),
        team_name=config.get('team_name', None),
        service=lp)


if __name__ == "__main__":
    import pprint
    import random
    import string
    from .lp import Lp
    from .ppa_group import PpaGroup

    pp = pprint.PrettyPrinter(indent=4)

    print('##########################')
    print('## Ppa class smoke test ##')
    print('##########################')
    print()

    rndstr = str(''.join(random.choices(string.ascii_lowercase, k=6)))
    dep_name = f'dependency-ppa-{rndstr}'
    smoketest_ppa_name = f'test-ppa-{rndstr}'

    lp = Lp('smoketest', staging=True)
    ppa_group = PpaGroup(service=lp, name=lp.me.name)

    dep_ppa = ppa_group.create(dep_name, ppa_description=dep_name)
    the_ppa = ppa_group.create(smoketest_ppa_name, ppa_description=smoketest_ppa_name)
    ppa_dependencies = [f'ppa:{lp.me.name}/{dep_name}']

    try:
        the_ppa.set_publish(True)

        if not the_ppa.exists():
            print("Error: PPA does not exist")
            sys.exit(1)
        the_ppa.set_description("This is a testing PPA and can be deleted")
        the_ppa.set_publish(False)
        the_ppa.set_architectures(["amd64", "arm64"])
        the_ppa.set_dependencies(ppa_dependencies)

        print()
        print(f"name:          {the_ppa.name}")
        print(f"address:       {the_ppa.address}")
        print(f"str(ppa):      {the_ppa}")
        print(f"reference:     {the_ppa.archive.reference}")
        print(f"self_link:     {the_ppa.archive.self_link}")
        print(f"web_link:      {the_ppa.archive.web_link}")
        print(f"description:   {the_ppa.description}")
        print(f"has_packages:  {the_ppa.has_packages()}")
        print(f"architectures: {'/'.join(the_ppa.architectures)}")
        print(f"dependencies:  {','.join(the_ppa.dependencies)}")
        print(f"url:           {the_ppa.url}")
        print()

    except BadRequest as e:
        print(f"Error: (BadRequest) {str(e.content.decode('utf-8'))}")
    except Unauthorized as e:
        print(f"Error: (Unauthorized) {e}")

    answer = 'x'
    while answer not in ['y', 'n']:
        answer = input('Ready to cleanup (i.e. delete) temporary test PPAs? (y/n) ')
        answer = answer[0].lower()

    if answer == 'y':
        print("  Cleaning up temporary test PPAs...")
        the_ppa.destroy()
        dep_ppa.destroy()
        print("  ...Done")
