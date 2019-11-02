import pytest

from bastion.commands.misc import eight_ball

def test_question():
    answer = eight_ball.get_answer('ABC')
    assert (answer in eight_ball.CHOICES['NEGATIVE_CHOICES'] or
            answer in eight_ball.CHOICES['POSITIVE_CHOICES'] or
            answer in eight_ball.CHOICES['MAYBE_CHOICES'])

def test_weighted_positive():
    for _ in range(1000):
        answer = eight_ball.get_answer('ABC', [100, 0, 0])
        assert answer in  eight_ball.CHOICES['POSITIVE_CHOICES']


def test_weighted_negative():
    for _ in range(1000):
        answer = eight_ball.get_answer('ABC', [0, 100, 0])
        assert answer in eight_ball.CHOICES['NEGATIVE_CHOICES']


def test_weighted_maybe():
    for _ in range(1000):
        answer = eight_ball.get_answer('ABC', [0, 0, 100])
        assert answer in eight_ball.CHOICES['MAYBE_CHOICES']

def test_falsey_questions():
    with pytest.raises(ValueError):
        eight_ball.get_answer(None)
        eight_ball.get_answer('')
