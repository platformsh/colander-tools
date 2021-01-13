
from __future__ import absolute_import

import base64

from colander import SchemaType, null, Invalid, _
import six

from . import compat


class AbstractEncodedBytes(SchemaType):
    encoder = None
    decoder = None

    def serialize(self, node, appstruct):
        if appstruct is null:
            return null

        if not isinstance(appstruct, six.binary_type):
            raise Invalid(node, _("appstruct, currently type {}, must be a byte string ".format(type(appstruct))))

        return self.encoder(appstruct)  # noqa

    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null

        if not isinstance(cstruct, compat.string_types):
            raise Invalid(node, _("cstruct, currently type {}, must be a string".format(type(cstruct))))

        return self.decoder(cstruct)  # noqa


# We need all encoded values to end up being strings so we can generate JSON, that is why they are decoded to
# ascii - they are bs64 encoded strings, meaning they can always become ascii strings.
# On the other hand, colander needs this to be byte strings, that is why we simply return bytes from the
# decoder.

class Base16Bytes(AbstractEncodedBytes):
    encoder = staticmethod(lambda b: base64.b16encode(b).decode("ascii"))
    decoder = staticmethod(base64.b16decode)


class Base32Bytes(AbstractEncodedBytes):
    encoder = staticmethod(lambda b: base64.b32encode(b).decode("ascii"))
    decoder = staticmethod(base64.b32decode)


class Base64Bytes(AbstractEncodedBytes):
    encoder = staticmethod(lambda b: base64.standard_b64encode(b).decode("ascii"))
    decoder = staticmethod(base64.standard_b64decode)


class URLSafeBase64Bytes(AbstractEncodedBytes):
    encoder = staticmethod(lambda b: base64.urlsafe_b64encode(b).decode("ascii"))
    decoder = staticmethod(base64.urlsafe_b64decode)
