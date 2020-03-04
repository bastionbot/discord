import random

def _parse(dice):
    if dice is None:
        return (1, 6)
    try:
        qty, faces = dice.split('d')
    except ValueError:
        faces = sum(ord(ch) for ch in dice)
        qty = 1
    if not faces:
        raise ValueError(f'Cannot extract number of faces from {dice}.')
    if not str(faces).isdigit():
        faces = sum(ord(ch) for ch in dice)
    if not str(qty).isdigit():
        qty = sum(ord(ch) for ch in dice)
    if not qty:
        qty = 1
    return (int(qty), int(faces))

def roll(dice):
    qty, faces = _parse(dice)
    return list(map(random.randint, [1] * qty, [faces] * qty))
