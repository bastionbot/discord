import pytest

from bastion.commands.misc import roll_dice


def test_parse_none():
    """
    Passing Mone defaults to a 1 six-sided die.
    """
    qty, faces = roll_dice._parse(None)
    assert qty == 1
    assert faces == 6


def test_parse_qty_faces():
    qty, faces = roll_dice._parse('5d10')
    assert qty == 5
    assert faces == 10


def test_parse_faces():
    qty, faces = roll_dice._parse('d10')
    assert qty == 1
    assert faces == 10


def test_parse_fail():
    """
    If we can't extract the faces, we cannot proceed
    """
    with pytest.raises(ValueError):
        roll_dice._parse('10d')
        roll_dice._parse('d')


def test_roll():
    result = roll_dice.roll('20d10')
    assert len(result) == 20
    assert all((item >= 1 and item <= 10 for item in result))
