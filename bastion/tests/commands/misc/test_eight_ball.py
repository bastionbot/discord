import pytest

from bastion.commands.misc import eight_ball

def test_truthy_question():
    answer = eight_ball.get_answer('ABC')
    assert answer in eight_ball.CHOICES


def test_falsey_questions():
    with pytest.raises(ValueError):
        eight_ball.get_answer(None)
        eight_ball.get_answer('')
