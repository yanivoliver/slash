from setuptools import setup, find_packages
import functools
import os
import platform

_PYTHON_VERSION = platform.python_version()
_in_same_dir = functools.partial(os.path.join, os.path.dirname(__file__))

with open(_in_same_dir("slash", "__version__.py")) as version_file:
    exec(version_file.read())  # pylint: disable=W0122

install_requires = [
    "colorama",
    "confetti>=2.0.0.dev2",
    "logbook",
    "requests>=1.1.0",
    "six",
]

if _PYTHON_VERSION < "3.0":
    install_requires.append("raven")

if _PYTHON_VERSION < "2.7":
    install_requires.append("argparse")

setup(name="slash",
      classifiers = [
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          ],
      description="A Testing Framework",
      license="BSD",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),
      install_requires=install_requires,
      entry_points = dict(
          console_scripts = [
              "slash  = slash.frontend.main:main_entry_point",
              ]
          ),

      )
