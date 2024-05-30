from datetime import datetime, timezone

from pytest import approx, mark, raises
from shapely import Point

from tle_tools.satellite import Satellite, ViewAngles


def test_position_invalid_datetime(polar_tle):
    sat = Satellite(polar_tle)
    t = datetime(2024, 4, 19, 12, 0, 0, 0)

    with raises(ValueError, match="datetime must be in utc"):
        sat.position(t)


@mark.parametrize(
    "t, p",
    (
        (
            datetime(2024, 4, 19, 12, 0, 0, 0, timezone.utc),
            Point(152.6226382884999, 78.18538506762289, 557934.9901695348),
        ),
    ),
)
def test_position(polar_tle, t, p):
    sat = Satellite(polar_tle)

    pos = sat.position(t)

    assert pos.equals(p)


@mark.parametrize(
    "t,o,e",
    (
        (
            datetime(2024, 4, 19, 12, 0, 0, 0, timezone.utc),
            [-5, 0, 0],
            ViewAngles(-0.3, -11.5),
        ),
        (
            datetime(2024, 4, 19, 12, 0, 0, 0, timezone.utc),
            [5, 0, 0],
            ViewAngles(-0.7, 11.5),
        ),
    ),
)
def test_view_angles(polar_tle, t, o, e):
    sat = Satellite(polar_tle)
    p = sat.position(t)

    a = sat.view_angles(t, Point(p.x + o[0], p.y + o[1], o[2]))

    assert a.across == approx(e.across, abs=0.1)
    assert a.along == approx(e.along, abs=0.1)
