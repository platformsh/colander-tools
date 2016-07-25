import pytz
from pytz import exceptions

import colander


class TimezoneType(colander.SchemaType):
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null

        if not isinstance(appstruct, pytz.tzinfo.BaseTzInfo):
            raise colander.Invalid(
                node,
                colander._(
                    '"${val}" is not a known timezone',
                    mapping={"val": appstruct},
                ),
            )

        return appstruct.zone

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null

        try:
            return pytz.timezone(cstruct)
        except exceptions.UnknownTimeZoneError:
            raise colander.Invalid(
                node,
                colander._(
                    '"${val}" is an invalid timezone',
                    mapping={"val": cstruct},
                ),
            )
