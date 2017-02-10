import discord
import markov
import sys
import random
import re

corpus = []
client = discord.Client()
trump = ['trump', 'Trump']
trumps = ['Orangegropenfuhrer', 'hate mango', 'cheeto golem', 'Hair Furor', 'trumpster fire']
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    corpus[0] = markov.buildcorpus()
    print('Corpus built')
    print('------')

@client.event
async def on_message(message):
    msgcontent = message.content
    writecontent = msgcontent + '.\n'
    msgauthor = str(message.author)
    msg = []
    if not '274350023473496064' == message.author.id and not message.content.startswith('!') and 'BroBot' not in msgauthor:
        wfile = open("discord_corpus", "a")
        wfile.write(re.sub(r'<[@]?[&!]?[\d]*>','',writecontent))
        wfile.close()
    if message.content.startswith('!markov'):
        try:
            if message.content == '!markov':
                msg.insert(0, markov.sayrandomshit(corpus[0]))
            tmp = str(message.content).split(' ')
            if tmp[1] == 'tweet':
                msg = [ markov.sayrandomshit(corpus[0], '1') ]
            elif 0 < int(tmp[1]) <= 10 and tmp[1] != 'tweet':
                for i in range(int(tmp[1])):
                    msg.append(markov.sayrandomshit(corpus[0]))
        except ValueError:
            msg = [ 'Bad syntax. Use "!markov by itself or !markov tweet or !markov <number of lines> (1-10)' ]
        for send in msg:
            await client.send_message(message.channel, send)
    elif 'rad' in msgcontent:
        await client.send_message(client.get_channel('193536175451930624'), 'hell yeah')
    elif any(word in trump for word in msgcontent.split(" ")):
        await client.send_message(message.channel, '_'+trumps[random.randrange(0,5)]+'*_')

client.run("<bot key>")
