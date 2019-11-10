from bastion.commands.misc import is_art


def test_is_art_with_question():
    result = is_art.is_art('Thing')
    assert result[3:-4] in is_art.CHOICES # Let's trim the part that won't change


def test_is_art_without_question():
    result = is_art.is_art()
    assert result == is_art.DEFAULT_ANSWER
