# 0.4.0 #

Reverse dependencies, build dependencies, and installation dependencies
can be identified for a given source package using cached APT
information.  This list of packages will be used to generate lists of
autopkgtest triggers, which when run should help identify issues that
could get flagged in Britney2 runs.  While similar to functionality
provided by Bileto+Britney2, it is a lighterweight facsimile which
doesn't handle special cases so should not be considered an equivalent,
just as a preliminary screen to catch basic issues.

For now, users will need to create and maintain this cache by hand
(automatic caching is planned for 0.5).  See the README for a suggested
rsync command to do this.

In addition, The `ppa set` command now supports a number of new command
line options.  `--ppa-dependencies` allows you to specify that your PPA
can use the contents of one or more other PPAs to satisfy build
dependencies.  The `--architectures` option now has some related options
`--all-architectures` and `--default-architectures` for "Give me
everything" and "Just the usual", respectively.  The `--enable` and
`--disable` arguments control whether packages can be uploaded to the
PPA to build.

All of the options supported by `ppa set` can also be specified to `ppa
create` to allow specifying them at creation time.

Beyond these two features, notable bugfixes address problems with Ubuntu
release specification, improvements to the `ppa tests` output, and
various idiosyncrasies with command line arguments.


# 0.3.0 Release #

Autopkgtest trigger action URLs are printed for packages in the PPA when
running the `ppa tests` command.  Both plain and 'all-proposed' style
triggers are displayed.  These can be loaded in a web browser by someone
with core-dev permissions to start the test runs.  `ppa tests` can then
be re-run to check on the tests status and results.

Most commands now accept the PPA identifier as a URL, as well as a
formal PPA address, or just the basic name of the PPA, which will be
assumed to be in the user's namespace.

New options are now available for a few commands.  The option parsing
and handling has been significantly reworked to allow per-command arg
shortcuts, so for instance -r can mean one thing for the 'create'
command and something completely different for the 'wait' command.


# 0.2.1 Release #

This corrects some packaging issues when generating .deb and .snap
packages:  Some missing build-dependencies are added, and some path
adjustments included to ensure the script is able to import the
installed python modules when installed in a snap environment.


# 0.2.0 Release #

This release adds a new 'tests' command that lists any pending or
waiting test runs against the PPA at autopackage.canonical.com.  This
functionality is integrated from Christian Ehrhardt's `lp-test-ppa`
tool[1], coupled with new test cases, code documentation, and
pylint/flake style improvements.  The new command is run like this:

    $ ppa tests ppa:my-name/my-ppa

The second major focus for this release was to refine and solidify the
packaging and installation process.  In addition to PyPI, this will be
packaged as a snap and as a debian package via PPA (of course!)

1: https://git.launchpad.net/~ubuntu-server/+git/ubuntu-helpers/tree/cpaelzer/lp-test-ppa



# 0.1.0 Release #

A core set of commands including create, destroy, wait, list, and show
are implemented, along with basic help and package docs.  The
intent of this release is to get registered with PyPI and scope out the
release process.

Here's an example set of commands one might use:

   $ ppa create my-ppa
   $ dput ppa:my-name/my-ppa some-package.changes
   $ ppa wait my-ppa
   $ cat some-package/README | ppa desc ppa:my-name/my-ppa
   $ ppa destroy my-ppa

This creates a PPA and uploads a package to it.  Then it waits for the
package to complete building and then updates the PPA's description with
some user-provided information.  At this point the PPA might be shared
with users or used for testing purposes.  Finally, when no longer needed
it is removed.
