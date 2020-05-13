import random

CHOICES = [
    '**{thing}**, now get out there and put those pucks in the net.',
    "DO IT!! JUST DO IT!! Don't let your **{thing}** dreams be dreams.",
    '\\*nuzzles ur **{thing}**\\*',
    '**{thing}** is the single best idea I\'ve ever heard, yo.',
    'The world must **{thing}**.',
    "**{thing}** is kickin' rad!",
    'The high council has concluded that **{thing}** is it, chief.',
    '**{thing}** might be good, yeah.',
    '**{thing}** is fucked up. Hell yeah.',
    "**{thing}** ain't the coolest, but that's just my opinion.",
    "Extra! Extra! Read all about **{thing}**!",
    'Duh, **{thing}**.',
    'Obviously **{thing}**.',
    'Definitely **{thing}**.',
    'Verily, I counsel thee for **{thing}**.',
    '**{thing}** smothered in sausage gravy, with a side of hashbrowns, and slices of bacon.',
    '**{thing}** was elected class president!',
    'This just in, **{thing}** is the new hotness!'
]

NOT_ENOUGH_OPTIONS_PHRASE = 'I need to have at least two options!'


def _split_items(options):
    return options.split(' or ')


def _pick_thing_phrase(option):
    phrase = random.choice(CHOICES)
    return phrase.format(thing=option)


def decide(options):
    if not options:
        raise ValueError(NOT_ENOUGH_OPTIONS_PHRASE)

    items = _split_items(options)
    if len(items) == 1:
        raise ValueError(NOT_ENOUGH_OPTIONS_PHRASE)

    return _pick_thing_phrase(random.choice(items))
