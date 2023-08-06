# sd212review
Simple Python module to tell you which unit to write review questions for SD212

# Usage

    from sd212review import whichunit

    # you can call it with a number
    whichunit(257863) # returns 2

    # or you can call it with a string
    whichunit('m264351') # returns 3

# Build instructions

Follow [this tutorial on packaging](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
and [this quickstart for setuptools](https://setuptools.pypa.io/en/latest/userguide/quickstart.html).

Pip/conda/mamba packages needed:

    build twine

To test:

    python3 test.py

To build:

    python3 -m build

To publish on pypi (requires account setup and
[api token](https://test.pypi.org/manage/account/token/)):

    python3 -m twine upload --repository testpypi dist/*
