import discord
import markov
import random
import re
import sys
import os
import twitter

os.chdir('/usr/local/bin/discord')
with open('twitkeys') as f:
    lines = f.readlines()
api = twitter.Api(consumer_key=lines[0].strip(), 
                  consumer_secret=lines[1].strip(),
                  access_token_key=lines[2].strip(),
                  access_token_secret=lines[3].strip())
f = open("botkey", 'r')
botkey = str(f.readline())
f.close()
corpus = [""]
botkey = botkey.rstrip()
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global corpus
    corpus[0] = markov.buildcorpus()
    print('Corpus built')
    print('------')
    await client.send_message(client.get_channel('193536175451930624'), 'Bastionbot restarted')

@client.event
async def on_message(message):
    msgcontent = message.content
    writecontent = msgcontent + '\n'
    msgauthor = str(message.author)
    msg = []
    if not '274350023473496064' == message.author.id and not message.content.startswith('!') and 'BroBot' not in msgauthor:
        wfile = open("discord_corpus", "a")
        wfile.write(re.sub(r'<[@]?[&!]?[\d]*>','',writecontent))
        wfile.close()
    if message.content.startswith('!tweet'):
        try:
            tweet = api.PostUpdate(markov.sayrandomshit(corpus[0], 1))
            twitmsg = "https://twitter.com/SRSOC_Bastion/status/"+tweet.id_str
            await client.send_message(message.channel, twitmsg)
        except:
            await client.send_message(message.channel, 'Failed to tweet :saddowns:')
    if message.content.startswith('!markov'):
        try:
            tmp = str(message.content).split(' ')
            uarg = len(tmp)
            if uarg == 1:
                msg.insert(0, markov.sayrandomshit(corpus[0]))
            if uarg == 2:
                msg = [ markov.sayrandomshit(corpus[0], tmp[1]) ]
        except ValueError:
            msg = [ 'Bad syntax. Use "!markov by itself or !markov tweet or !markov <number of lines> (1-10)' ]
        for send in msg:
            await client.send_message(message.channel, send)

client.run(botkey)
