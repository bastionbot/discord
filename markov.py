import markovify


def buildcorpus(state=3):
    with open("discord_corpus") as r:
       wcorpus = r.read()
    text_model = markovify.Text(wcorpus, state_size=state)
    model_json = text_model.to_json()
    f = open("corpus.json", 'w+')
    f.write(model_json)
    f.truncate()
    f.seek(0)
    return markovify.Text.from_json(f.read())

def sayrandomshit(model=None, tw=None):
    if tw is not None:
        return model.make_short_sentence(140)
    return buildphrase(model)

def buildphrase(jsonmodel):
    phrase = None
    while phrase is None:
        phrase = jsonmodel.make_sentence()
    return phrase
