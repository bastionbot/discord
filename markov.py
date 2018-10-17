import markovify
import sched
import datetime
import time
import sqlite3
import re

def buildcorpus(state=3, db): #This is currently broken.
    wcorpus = []
    c = db.cursor()
    for x in c.execute("SELECT message FROM chathistory WHERE date >?",datetime.timedelta(days=-7)):
        removeLinks = re.sub(r'http\S+', '', x)
        wcorpus.append(re.sub(r'<[@]?[&!]?[\d]*>','', removeLinks))
    text_model = markovify.NewlineText(wcorpus, state_size=state)
    model_json = text_model.to_json()
    f = open("corpus.json", 'w+')
    f.write(model_json)
    f.truncate()
    f.seek(0)
    return

def getcorpus(): #unused (yet)
    return markovify.Text.from_json(open("corpus.json").read())

def sayrandomshit(model, message):
    phrase = None
    try:
        keyword = " ".join(message.split()[1:].strip())
    except:
        keyword = None
    while phrase is None:
        #if keyword is not None:
            #try:
            #    phrase = model.make_sentence_with_start(keyword).split('___BEGIN__')[1]
            #except:
            #    phrase = "Through no fault of my own, that didn't work."
        #else:
        phrase = model.make_sentence()
    if "http" in phrase:
        phrase = model.make_sentence()
    return phrase

def sayrandomtweet(model):
    phrase = None
    while phrase is None:
        phrase = model.make_short_sentence(140)
    if "http" in phrase:
        sayrandomtweet(model)
    return phrase
