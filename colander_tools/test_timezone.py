import datetime

import pytz
import pytest
import colander
from colander_tools import timezone


def test_timezone():
    tz = timezone.TimezoneType().serialize({}, pytz.timezone("Europe/Paris"))
    assert(tz == "Europe/Paris")

    tz = timezone.TimezoneType().deserialize({}, "Europe/Paris")
    normal = datetime.datetime(2009, 9, 1)

    assert(tz.tzname(normal) == "CEST")

    with pytest.raises(colander.Invalid):
        timezone.TimezoneType().serialize({}, "Foo/Bar")

    with pytest.raises(colander.Invalid):
        # Not a timezone object
        timezone.TimezoneType().serialize({}, "Europe/Paris")

    with pytest.raises(colander.Invalid):
        timezone.TimezoneType().deserialize({}, "Foo/Bar")
