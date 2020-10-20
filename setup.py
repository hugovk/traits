# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import os
import runpy
import subprocess

import setuptools

# Version information; update this by hand when making a new bugfix or feature
# release. The actual package version is autogenerated from this information
# together with information from the version control system, and then injected
# into the package source.
MAJOR = 6
MINOR = 2
MICRO = 0
PRERELEASE = ""
IS_RELEASED = False

# If this file is part of a Git export (for example created with "git archive",
# or downloaded from GitHub), ARCHIVE_COMMIT_HASH gives the full hash of the
# commit that was exported.
ARCHIVE_COMMIT_HASH = "$Format:%H$"

# Templates for version strings.
RELEASED_VERSION = "{major}.{minor}.{micro}{prerelease}"
UNRELEASED_VERSION = "{major}.{minor}.{micro}{prerelease}.dev{dev}"

# Paths to the autogenerated version file and the Git directory.
HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(HERE, "traits", "version.py")
GIT_DIRECTORY = os.path.join(HERE, ".git")

# Template for the autogenerated version file.
VERSION_FILE_TEMPLATE = '''\
# (C) Copyright 2005-2020 {company}, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Version information for this Traits distribution.

This file is autogenerated by the Traits setup.py script.
"""

#: The full version of the package, including a development suffix
#: for unreleased versions of the package.
version = "{version}"

#: The Git revision from which this release was made.
git_revision = "{git_revision}"
'''

# Git executable to use to get revision information.
GIT = "git"


def _git_output(args):
    """
    Call Git with the given arguments and return the output as text.
    """
    return subprocess.check_output([GIT] + args).decode("utf-8")


def _git_info(commit="HEAD"):
    """
    Get information about the given commit from Git.

    Parameters
    ----------
    commit : str, optional
        Commit to provide information for. Defaults to "HEAD".

    Returns
    -------
    git_count : int
        Number of revisions from this commit to the initial commit.
    git_revision : str
        Commit hash for HEAD.

    Raises
    ------
    EnvironmentError
        If Git is not available.
    subprocess.CalledProcessError
        If Git is available, but the version command fails (most likely
        because there's no Git repository here).
    """
    count_args = ["rev-list", "--count", "--first-parent", commit]
    git_count = int(_git_output(count_args))

    revision_args = ["rev-list", "--max-count", "1", commit]
    git_revision = _git_output(revision_args).rstrip()

    return git_count, git_revision


def write_version_file(version, git_revision):
    """
    Write version information to the version file.

    Overwrites any existing version file.

    Parameters
    ----------
    version : str
        Package version.
    git_revision : str
        The full commit hash for the current Git revision.
    """
    with open(VERSION_FILE, "w", encoding="utf-8") as version_file:
        version_file.write(
            VERSION_FILE_TEMPLATE.format(
                version=version, git_revision=git_revision, company="Enthought"
            )
        )


def read_version_file():
    """
    Read version information from the version file, if it exists.

    Returns
    -------
    version : str
        The full version, including any development suffix.
    git_revision : str
        The full commit hash for the current Git revision.

    Raises
    ------
    EnvironmentError
        If the version file does not exist.
    """
    version_info = runpy.run_path(VERSION_FILE)
    return (version_info["version"], version_info["git_revision"])


def git_version():
    """
    Construct version information from local variables and Git.

    Returns
    -------
    version : str
        Package version.
    git_revision : str
        The full commit hash for the current Git revision.

    Raises
    ------
    EnvironmentError
        If Git is not available.
    subprocess.CalledProcessError
        If Git is available, but the version command fails (most likely
        because there's no Git repository here).
    """
    git_count, git_revision = _git_info()
    version_template = RELEASED_VERSION if IS_RELEASED else UNRELEASED_VERSION
    version = version_template.format(
        major=MAJOR,
        minor=MINOR,
        micro=MICRO,
        prerelease=PRERELEASE,
        dev=git_count,
    )
    return version, git_revision


def archive_version():
    """
    Construct version information for an archive.

    Returns
    -------
    version : str
        Package version.
    git_revision : str
        The full commit hash for the current Git revision.

    Raises
    ------
    ValueError
        If this does not appear to be an archive.
    """
    if "$" in ARCHIVE_COMMIT_HASH:
        raise ValueError("This does not appear to be an archive.")

    version_template = RELEASED_VERSION if IS_RELEASED else UNRELEASED_VERSION
    version = version_template.format(
        major=MAJOR,
        minor=MINOR,
        micro=MICRO,
        prerelease=PRERELEASE,
        dev="-unknown",
    )
    return version, ARCHIVE_COMMIT_HASH


def resolve_version():
    """
    Process version information and write a version file if necessary.

    Returns the current version information.

    Returns
    -------
    version : str
        Package version.
    git_revision : str
        The full commit hash for the current Git revision.
    """
    if os.path.isdir(GIT_DIRECTORY):
        # This is a local clone; compute version information and write
        # it to the version file, overwriting any existing information.
        version = git_version()
        print("Computed package version: {}".format(version))
        print("Writing version to version file {}.".format(VERSION_FILE))
        write_version_file(*version)
    elif "$" not in ARCHIVE_COMMIT_HASH:
        # This is a source archive.
        version = archive_version()
        print("Archive package version: {}".format(version))
        print("Writing version to version file {}.".format(VERSION_FILE))
        write_version_file(*version)
    elif os.path.isfile(VERSION_FILE):
        # This is a source distribution. Read the version information.
        print("Reading version file {}".format(VERSION_FILE))
        version = read_version_file()
        print("Package version from version file: {}".format(version))
    else:
        raise RuntimeError(
            "Unable to determine package version. No local Git clone "
            "detected, and no version file found at {}.".format(VERSION_FILE)
        )

    return version


def get_long_description():
    """ Read long description from README.txt. """
    with open("README.rst", "r", encoding="utf-8") as readme:
        return readme.read()


version, git_revision = resolve_version()

setuptools.setup(
    name="traits",
    version=version,
    url="http://docs.enthought.com/traits",
    author="Enthought",
    author_email="info@enthought.com",
    classifiers=[
        c.strip()
        for c in """
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        Intended Audience :: Science/Research
        License :: OSI Approved :: BSD License
        Operating System :: MacOS :: MacOS X
        Operating System :: Microsoft :: Windows
        Operating System :: POSIX :: Linux
        Programming Language :: Python
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: 3.7
        Programming Language :: Python :: 3.8
        Programming Language :: Python :: 3.9
        Programming Language :: Python :: Implementation :: CPython
        Topic :: Scientific/Engineering
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        Topic :: Software Development :: User Interfaces
        """.splitlines()
        if len(c.strip()) > 0
    ],
    description="Observable typed attributes for Python classes",
    long_description=get_long_description(),
    long_description_content_type="text/x-rst",
    download_url="https://pypi.python.org/pypi/traits",
    project_urls={
        "Issue Tracker": "https://github.com/enthought/traits/issues",
        "Documentation": "https://docs.enthought.com/traits",
        "Source Code": "https://github.com/enthought/traits",
    },
    install_requires=[],
    extras_require={
        "docs": [
            "enthought-sphinx-theme",
            "Sphinx!=3.2.0",
        ],
        "test": [
            "Cython",
            "flake8",
            "mypy",
            "setuptools",
            "Sphinx!=3.2.0",
            # Python 3.9 exclusions:
            #
            # * NumPy installation fails on Python 3.9 on the Ubuntu Xenial
            #   system used by Travis CI.
            # * PySide2 is installable but also currently not working
            #   on Python 3.9.
            # * Because of the above, we also exclude GUI-using packages
            #   Pyface and TraitsUI on Python 3.9.
            "numpy;python_version<'3.9'",
            "pyface;python_version<'3.9'",
            "PySide2;python_version<'3.9'",
            "traitsui;python_version<'3.9'",
        ],
        "examples": [
            # dependencies for examples
            "numpy",
            "pillow",
        ]
    },
    ext_modules=[setuptools.Extension("traits.ctraits", ["traits/ctraits.c"])],
    package_data={
        "traits": [
            "examples/introduction/images/*",
        ],
        "traits.tests": [
            "test-data/historical-pickles/README",
            "test-data/historical-pickles/*.pkl",
            "test-data/historical-pickles/*.py",
        ],
    },
    entry_points={
        "etsdemo_data": [
            "introduction = traits.examples._entry_point:introduction",
        ],
    },
    license="BSD",
    packages=setuptools.find_packages(include=["traits", "traits.*"]),
    python_requires=">=3.6",
    zip_safe=False,
)
