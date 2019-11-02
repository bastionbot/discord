import random

def _parse(dice):
    if dice is None:
        return (1, 6)
    qty, faces = dice.split('d')
    if not faces:
        raise ValueError(f'Cannot extract number of faces from {dice}.')
    if not qty:
        qty = 1
    return (int(qty), int(faces))

def roll(dice):
    qty, faces = _parse(dice)
    return list(map(random.randint, [1] * qty, [faces] * qty))
