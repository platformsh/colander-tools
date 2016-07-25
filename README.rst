Colander Tools
====================================

This package is a set of extensions to ``colander`` especially useful when
implementing REST APIs.


Strict types
-------------------

The ``colander_tools.strict`` module includes a series of strict types. Those types
follow the `Postel's law <https://en.wikipedia.org/wiki/Robustness_principle>`_:
they are strict on serialize and loose on deserialize.

Included are:

* ``Integer``
* ``Float``
* ``Boolean``
* ``String``
* ``Mapping``


Byte types
-------------------

The ``colander_tools.bytes`` module includes types serializing / deserializing encoded binary data.

Included are:

* ``Base16Bytes``
* ``Base32Bytes``
* ``Base64Bytes``
* ``URLSafeBase64Bytes``


Open mappings
-------------------

The ``colander_tools.mapping`` module includes two ``Mapping`` subclasses that allow
and validate arbitrary keys in addition to the values.

Included are:

* ``OpenMapping``: a mapping that allows you to specify the type of keys and the type of values
  separately;
* ``SortedOpenMapping``: an extension of ``OpenMapping`` that conserve the order of keys by
  deserializing to ``collections.OrderedDict``.


Network addresses types
------------------------------

The ``colander_tools.netaddr`` module includes a series of types that serializes and
deserializes network addresses (IP addresses, MAC addresses, etc.), powered by the
``netaddr`` package.


Null types
-------------------

The ``colander_tools.null`` module includes a wrapper type that allows `None` as a value.


Serializable classes
------------------------------

The ``colander_tools.serializable`` module includes tools to bind Python classes
to their schema.


Schema inheritance / sub-schemas
-----------------------------------

The ``colander_tools.subschema`` module includes tools to build schemas of things
that can have different types / classes.


Timezone type
-------------------

The ``colander_tools.timezone`` module includes a type for serializing and
deserializing timezone identifiers like `Europe/Amsterdam` or `Asia/Hong_Kong`,
powered by the ``pytz`` package.
