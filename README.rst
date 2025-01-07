====
Inheritance Graph
====

|pypi| |py_versions|

.. |pypi| image:: https://img.shields.io/pypi/v/inheritance_graph
   :alt: PyPI - Version

.. |py_versions| image:: https://img.shields.io/pypi/pyversions/inheritance_graph
   :alt: PyPI - Python Version

.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python

A tool to help debug inheritance failures.

----
Example
----

.. code-block:: python

    from inheritance_graph import mro_check

    class Dec:
        pass

    class Dif:
        pass

    class E:
        pass

    class R(E):
        pass

    class Err(Dif, R):
        pass

    class B(E, Dec, Dif):
        pass

Suppose, you now try:

.. code-block:: python

    class Z(B, Err):
        pass

Then, Python merely says:

::

    TypeError: Cannot create a consistent method resolution order (MRO) for bases E, Dif

But if you call:

.. code-block:: python

    mro_check((B, Err))

it displays

::

    Cycle found:
       Dif precedes R in Err's MRO (and Err was in the proposed based class list) because
         Dif is a base class of Err
         R is a base class of Err
       R precedes E because it inherits from it directly.
       E precedes Dec in B's MRO (and B was in the proposed based class list) because
         E is a base class of B
         Dec is a base class of B
       Dec precedes Dif in B's MRO (and B was in the proposed based class list) because
         Dec is a base class of B
         Dif is a base class of B

-----------------------
Contribution guidelines
-----------------------

- Conventions: PEP8.

- How to clean the source:

  - :bash:`ruff check .`
  - :bash:`pyright`
  - :bash:`mypy`
  - :bash:`isort .`
  - :bash:`pylint inheritance_graph`
