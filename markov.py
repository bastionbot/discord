import markovify

def buildcorpus( output="corpus.json", state=3 ):
	with open("discord_corpus") as r:
		corpus = r.read()
	text_model = markovify.Text(corpus, state_size=state)
	model_json = text_model.to_json()
	with open("corpus.json", 'w+') as f:
		f.seek(0)
		f.write(model_json)
		f.truncate()

def sayrandomshit( file='corpus.json', tw = None ):
	with open(file) as f:
		text = f.read()
	model = markovify.Text.from_json(text)
	if tw is not None:
		return model.make_short_sentence(140)
	return buildphrase(model)

def buildphrase(jsonmodel):
	phrase = None
	while phrase is None:
		phrase = jsonmodel.make_sentence()
	return phrase
