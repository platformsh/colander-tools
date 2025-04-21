import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    string_types = (basestring,)  # noqa
    text_type = unicode  # noqa
else:
    string_types = (str,)  # noqa
    text_type = str  # noqa
