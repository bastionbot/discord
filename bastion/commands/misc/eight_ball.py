import random

CHOICES = {
    'POSITIVE_CHOICES': [
        'Yes.',
        'Yeah.',
        'Sure.',
        'This is Chill and Good.',
        'Absolutely.',
        'Do iiiiit. OwO',
        'Hell yeah, mother humper!',
        'Yeah sure, why not.',
        'Fuck yeah!',
        'Yeah, why not.',
        'It is certain.',
        'It is decidedly so.',
        'Most likely.',
        'As I see it, yes.',
        'Outlook good.',
        'Signs point to yes.',
        'Yes.',
        'Yes – definitely.',
        'You may rely on it.'
        'Without a doubt.',
    ],
    'NEGATIVE_CHOICES': [
        'No.',
        'Nah.',
        'nOwO.',
        "No fuckin' way, man.",
        'No. No! Absolutely not!',
        'Fuck no!',
        'OwO not today!!!',
        'Probably not.',
        "That's not very cash money.",
        "Yeah, that's gonna be a no from me, dog.",
        'Don’t count on it.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.',
    ],
    'MAYBE_CHOICES': [
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
    ],
}

DEFAULT_WEIGHTS = [50, 25, 25]

def get_answer(question, weigths=None):
    if not question:
        raise ValueError('An answer without a question is meaningless.')
    if weigths is None:
        weigths = DEFAULT_WEIGHTS
    # random.choices returns a list with size k (default 1), so the key is the first element
    key = random.choices(['POSITIVE_CHOICES', 'NEGATIVE_CHOICES', 'MAYBE_CHOICES'], weigths)[0]
    return random.choice(CHOICES[key])

