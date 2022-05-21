Contributing
--------------

How to request features
==============================
1. Talk to McClain or Ethan
2. Make a ticket in the Notion project management tab for this repo

How to request bug fixes
============================
1. Report it the github `issues <https://github.com/WealtHawk-prod/WH_Utils/issues>`_ tab for this repo

How to write code
==================
If you want to fix an issue or add a feature yourself, follow these steps.

Design
******
Make sure your design pattern / bug fix is consistent with the rest of the repo. For the most part
this just means don't do anything dumb. Don't print from functions, use exceptions. Use enums and
not strings. Use prebuilt abstractions if possible. Ect.

Documentation
***************
Document your code. I swear, if you don't document your code, the PR is getting rejected. Use the
`Google python style guide <https://google.github.io/styleguide/pyguide.html>`_ when documenting.
To see what your documentation looks like in the sphinx site you can run:

    `sphinx-build -b html build_docs docs`

This will generate the docs and dump them in the `docs` folder. Open the index.html file in that folder in
browser and you can see the full website. Make sure it looks how you want it to before you PR.
