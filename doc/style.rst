.. Copyright (c) 2016-2022 The Regents of the University of Michigan
.. Part of GSD, released under the BSD 2-Clause License.

Code style
==========

All code in GSD must follow a consistent style to ensure readability. We provide configuration files
for linters (specified below) so that developers can automatically validate and format files.

These tools are configured for use with `pre-commit`_ in ``.pre-commit-config.yaml``. You can
install pre-commit hooks to validate your code. Checks will run on pull requests. Run checks
manually with::

    pre-commit run --all-files

.. _pre-commit: https://pre-commit.com/

Python
------

Python code in GSD should follow `PEP8`_ with the formatting performed by `yapf`_ (configuration in
``setup.cfg``). Code should pass all **flake8** tests and formatted by **yapf**.

.. _PEP8: https://www.python.org/dev/peps/pep-0008
.. _yapf: https://github.com/google/yapf

Tools
^^^^^

* Linter: `flake8 <http://flake8.pycqa.org/en/latest/>`_

  * With these plugins:

    * `pep8-naming <https://github.com/PyCQA/pep8-naming>`_
    * `flake8-docstrings <https://gitlab.com/pycqa/flake8-docstrings>`_
    * `flake8-rst-docstrings <https://github.com/peterjc/flake8-rst-docstrings>`_

  * Configure flake8 in your editor to see violations on save.

* Autoformatter: `yapf <https://github.com/google/yapf>`_

  * Run: ``pre-commit run --all-files`` to apply style changes to the whole
    repository.

Documentation
^^^^^^^^^^^^^

Python code should be documented with docstrings and added to the Sphinx documentation index in
``doc/``. Docstrings should follow `Google style`_ formatting for use in `Napoleon`_.

.. _Google Style: https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google
.. _Napoleon: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

C
---

* Style is set by clang-format=11

  * Whitesmith's indentation style.
  * 100 character line width.
  * Indent only with spaces.
  * 4 spaces per indent level.
  * See :file:`.clang-format` for the full **clang-format** configuration.

* Naming conventions:

  * Functions: lowercase with words separated by underscores
    ``function_name``.
  * Structures: lowercase with words separated by underscores
    ``struct_name``.
  * Constants: all upper-case with words separated by underscores
    ``SOME_CONSTANT``.

Tools
^^^^^

* Autoformatter: `clang-format <https://clang.llvm.org/docs/ClangFormat.html>`_.

* Linter: `clang-tidy <https://clang.llvm.org/extra/clang-tidy/>`_

  * Compile **GSD** with **CMake** to see **clang-tidy** output.

Documentation
^^^^^^^^^^^^^

Documentation comments should be in Javadoc format and precede the item they document for
compatibility with Doxygen and most source code editors. Multi-line documentation comment blocks
start with ``/**`` and single line ones start with ``///``.

See :file:`gsd.h` for an example.

Restructured Text/Markdown files
--------------------------------

* 80 character line width.
* Use spaces to indent.
* Indentation levels are set by the respective formats.

Other file types
----------------

Use your best judgment and follow existing patterns when styling CMake and other files types. The
following general guidelines apply:

* 100 character line width.
* 4 spaces per indent level.
* 4 space indent.

Editor configuration
--------------------

`Visual Studio Code <https://code.visualstudio.com/>`_ users: Open the provided workspace file
(``gsd.code-workspace``) which provides configuration settings for these style guidelines.
