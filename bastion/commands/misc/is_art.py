import random

CHOICES = [
    'most certainly is',
    'definitely is',
    'absolutely is not',
    'possibly could be',
    'is not at all',
    'is',
    'is not',
    'could not be',
    'could be nothing other than'
]

DEFAULT_ANSWER = 'Art is everywhere'

def is_art(question=None):
    if not question:
        return DEFAULT_ANSWER
    return f'It {random.choice(CHOICES)} art'
