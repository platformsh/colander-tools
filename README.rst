Colander Tools
====================================

This package is a set of extensions to ``colander`` especially useful when
implementing REST APIs.


Strict types
-------------------

The ``colander_tools`` package includes a series of strict types. Those types
follow the `Postel's law <https://en.wikipedia.org/wiki/Robustness_principle>`_:
they are strict on serialize and loose on deserialize.

Included are:

 * Integer
 * Float
 * Boolean
 * String
