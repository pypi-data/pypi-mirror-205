Releasing a New PPA Dev Tools Version
=====================================

Before you start
----------------

* Update local Git repository to the current `main` tip.  For a
  maintenance release (e.g. version 1.2.3), update to the current
  `stable-1.2` tip, instead.

* Commit everything that needs included in the release

* Doublecheck all new dependencies are specified in packaging
  $ grep -h import */* | sed 's/    //' | grep -vE '(import|from) (ppa|\.)' | sort -u

* Doublecheck the INSTALL.md file is still up to date

* Verify the build system works without errors
  $ make build

* Verify the testsuite, lint, flake, etc. passes
  $ make check
  $ make coverage

* Verify the snapcraft config is ready
  $ snapcraft --debug
  $ rm *.snap

* Cleanup
  $ make clean
  $ git status --ignored

* Write an entry in NEWS.md file with release notes


Generate the source release
---------------------------

* Set the version
  $ export VERSION="X.Y.Z"
  $ make set-release-version

* Add the release collateral
  $ git commit NEWS.md ppa/_version.py pyproject.toml snap/snapcraft.yaml -m "Releasing ${VERSION}"
  $ git tag -a -m "PPA Dev Tools ${VERSION}" "v${VERSION}"

* Push the release
  $ git push origin main "v${VERSION}"

* Create the release directory
  $ cp -ir ../$(basename $(pwd)) ../Releases/ppa-dev-tools-${VERSION}/
  $ cd ../Releases/ppa-dev-tools-${VERSION}

* Generate the release tarball
  $ make build
  $ python3 -m twine upload --verbose --repository pypi dist/*-${VERSION}*


Generate the debian package
---------------------------

* Set to latest distro release, and add changelog entry for "New release"
  $ dch -v "${VERSION}"
  $ debuild -S -sa
  $ dput ppa:bryce/ppa-dev-tools ../ppa-dev-tools_${VERSION}_source.changes

* Repeat for each LTS release, with version set to ${VERSION}~YY.MM.N
  and changelog entry "Backport for ${codename}"
  $ dput ppa:bryce/ppa-dev-tools ../ppa-dev-tools_${VERSION}~YY.MM.N_source.changes


Generate the snap
-----------------

* Build the snap locally
  $ make snap

* Verify the snap
  $ sudo snap install ppa-dev-tools_<version>_amd64.snap --devmode
  ppa-dev-tools <version> installed
  $ /snap/ppa-dev-tools/current/bin/ppa --version

* Push snap to the snap repository
  $ snapcraft login
  $ snapcraft upload --release edge *.snap

* Push the tag up to the repository


Announce release
----------------

* Add release announcement on Launchpad
* Send email to appropriate list(s)
* Update roadmap


Return to Development
---------------------

* Add a final commit bumping the package version to a new development one

* Finally, a manual `git push` (including tags) is required.
