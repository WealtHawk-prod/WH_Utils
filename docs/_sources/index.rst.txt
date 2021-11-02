WH_Utils
---------

|Read the Docs| |Tests| |pre-commit| |Black|


.. |Read the Docs| image:: https://img.shields.io/badge/Docs-Here-blue.svg
   :target: https://mcclain-thiel.github.io/WH_Utils/
   :alt: Read the documentation at https://mcclain-thiel.github.io/WH_Utils/
.. |Tests| image:: https://github.com/McClain-Thiel/WH_Utils/workflows/Tests/badge.svg
   :target: https://github.com/McClain-Thiel/WH_Utils/actions?workflow=Tests
   :alt: Tests
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


What is it?
---------------

The `WH_Utils` repo is meant to make development easier across the organization by standardizing the way
we interact with common objects. For example, there are modules for `Objects` that contain all enums used
by the organization and a `Models` module that contains a powerful class based representation of common
objects. For more info on this check out the docs.

How to install
-------------------

``python -m pip install git+https://github.com/django/django.git@45dfb3641aa4d98``

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





.. include:: README.rst
   :end-before: github-only

.. _Usage: usage.html


.. toctree::
   :hidden:
   :maxdepth: 1

   usage
   reference

