import markovify


def buildcorpus(state=3):
    with open("discord_corpus") as r:
        corpus = r.read()
    text_model = markovify.Text(corpus, state_size=state)
    model_json = text_model.to_json()

    f = open("corpus.json", 'w+')

    f.seek(0)
    f.write(model_json)
    f.truncate()
    model = markovify.Text.from_json(f.read())

    return model


def sayrandomshit(model=None, tw=None):
    if tw is not None:
        return model.make_short_sentence(140)
    return buildphrase(model)

def buildphrase(jsonmodel):
    phrase = None
    while phrase is None:
        phrase = jsonmodel.make_sentence()
    return phrase
