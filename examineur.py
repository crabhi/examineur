#!/usr/bin/env python3
"""
Tests Jupyter notebook.

Specify a test suite and a notebook (or its URL). Examineur will convert
the notebook to Python code and test it.

To pass extra flags to pytest, specify them after "--", such as

./examineur.py example_tests.py example_nb.ipynb -- -v
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

import nbconvert
import pytest


def get_notebook(notebook, directory):
    nb_name = os.path.join(directory, 'tested_nb.ipynb')
    if re.match(r'^https?:.+', notebook):
        match = re.match(r'^.+://(www\.)?github\.com/([^/]+)/([^/]+)/blob/(.+)$', notebook)
        if match:
            notebook = f'https://raw.githubusercontent.com/{match.group(2)}/{match.group(3)}/{match.group(4)}'
        print(f'Downloading {notebook}', file=sys.stderr)
        buf = urllib.request.urlopen(notebook)
    else:
        buf = open(notebook, 'rb')

    try:
        with open(nb_name, 'wb') as localnb:
            shutil.copyfileobj(buf, localnb)
    finally:
        buf.close()

    return nb_name


def main(testfile, notebook, pytest_args):
    abs_testfile = os.path.abspath(testfile)
    with tempfile.TemporaryDirectory() as tmpdir:
        nb_name = get_notebook(notebook, tmpdir)
        subprocess.run(['jupyter-nbconvert', '--to', 'python', nb_name]).check_returncode()

        sys.path.insert(0, tmpdir)
        sys.exit(pytest.main([abs_testfile] + pytest_args))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('testfile', metavar='TESTS', help='Test suite. See example_tests.py.')
    parser.add_argument('notebook', metavar='NOTEBOOK', help='Path or URL to the notebook.')
    parser.add_argument('pytest_args', metavar='PYTEST_ARGS', nargs='*',
                        help='Additional arguments will be passed to pytest.')

    args = parser.parse_args()
    main(args.testfile, args.notebook, args.pytest_args)
