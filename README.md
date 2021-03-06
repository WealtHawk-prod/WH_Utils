WH_Utils
---------


[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Read the Docs](https://img.shields.io/badge/Docs-Here-blue.svg)](https://docs.wealthawk.com)
[![Tests](https://github.com/McClain-Thiel/WH_Utils/workflows/Tests/badge.svg)](https://github.com/McClain-Thiel/WH_Utils/actions?workflow=Tests)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Lines of Code](https://tokei.rs/b1/github/McClain-Thiel/WH_Utils)](https://github.com/McClain-Thiel/WH_Utils)

What is it?
---------------

The `WH_Utils` repo is meant to make development easier across the organization by standardizing the way
we interact with common objects. For example, there are modules for `Objects` that contain all enums used
by the organization and a `Models` module that contains a powerful class based representation of common
objects. For more info on this check out the docs.

How to install
-------------------

``python -m pip install git+https://github.com/WealtHawk-prod/WH_Utils``

How to Use
-------------

Check reference for documentation and usage for examples.

How to contribute
---------------------

1. ``python3 -m pip install --upgrade build``

2. ``python3 -m build``

3. Activate virtual env

4. ``pip3 install . pytest``

5. Get your API key from ``db.wealthawk.com`` and put it in ``tests/test_data/auth.json``

6. run ``pytest test``

7. If everything works, build the docs with ``sphinx-build build_docs docs``

8. If that builds correctly, just push to github as per usual.
