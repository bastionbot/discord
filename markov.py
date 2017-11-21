import markovify

def buildcorpus(state=3):
    with open("discord_corpus") as r:
       wcorpus = r.read()
    text_model = markovify.NewlineText(wcorpus, state_size=state)
    model_json = text_model.to_json()
    f = open("corpus.json", 'w+')
    f.write(model_json)
    f.truncate()
    f.seek(0)
    return markovify.Text.from_json(f.read())

def sayrandomshit(model, message):
    tries = 0
    phrase = None
    try:
        keyword= " ".join(message.split()[1:])
    except:
        keyword = None
    while phrase is None:
        if tries == 10:
            return "Failed to build phrase after 10 tries. Possible bad seed."
        if keyword is not None:
            try:
                phrase = model.make_sentence_with_start(keyword).split('___BEGIN__')[1]
            except:
                continue
        else:
            phrase = model.make_sentence()
        if "http" in phrase:
            phrase = None
        tries += 1
    return phrase

def sayrandomtweet(model):
    phrase = None
    while phrase is None:
        phrase = model.make_short_sentence(140)
    if "http" in phrase:
        sayrandomtweet(model)
    return phrase
