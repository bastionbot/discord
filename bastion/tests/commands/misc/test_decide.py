import pytest

from bastion.commands.misc import decide

def test_split_items():
    items = decide._split_items('x or y or z')
    assert items == ['x', 'y', 'z']

    items = decide._split_items('xory or z')
    assert items == ['xory', 'z']

    items = decide._split_items('x')
    assert items == ['x']


def test_thing_in_phrase():
    thing = 'SOMETHING HERE'
    phrase = decide._pick_thing_phrase(thing)
    assert thing in phrase # ¯\_(ツ)_/¯


def test_all_thing_phrases_formattable():
    thing = 'SOMETHING HERE'
    for phrase in decide.CHOICES:
        assert thing in phrase.format(thing=thing)


def test_decide():
    response = decide.decide('pizza or burger')

    assert ('burger' in response or
            'pizza' in response)


def test_decide_falsy():
    with pytest.raises(ValueError) as e:
        decide.decide(None)
        decide.decide('')
        assert str(e) == decide.NOT_ENOUGH_OPTIONS_PHRASE


def test_decide_one_option():
    with pytest.raises(ValueError) as e:
        response = decide.decide('pizza')
        assert str(e) == decide.NOT_ENOUGH_OPTIONS_PHRASE
