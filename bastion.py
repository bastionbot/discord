import discord
import markov
import random
import re

f = open("botkey", 'r')
botkey = str(f.readline())
f.close()
corpus = [""]
botkey = botkey.rstrip()
client = discord.Client()
trump = ['trump', 'Trump']
trumps = ['Orangegropenfuhrer', 'hate mango', 'cheeto golem', 'Hair Furor', 'trumpster fire']

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
    if message.content.startswith('!markov'):
        try:
            tmp = str(message.content).split(' ')
            uarg = len(tmp)
            if uarg == 1:
                msg.insert(0, markov.sayrandomshit(corpus[0]))
            if uarg == 2:
                msg = [ markov.sayrandomshit(corpus[0], tmp[1]) ]
 #           elif uarg == 2 and tmp[1] != 'tweet':
 #               for i in range(int(tmp[1])):
 #                   msg.append(markov.sayrandomshit(corpus[0]))
        except ValueError:
            msg = [ 'Bad syntax. Use "!markov by itself or !markov tweet or !markov <number of lines> (1-10)' ]
        for send in msg:
            await client.send_message(message.channel, send)
#    elif 'rad' in msgcontent:
 #       await client.send_message(client.get_channel('193536175451930624'), 'hell yeah')
    elif any(word in trump for word in msgcontent.split(" ")):
        await client.send_message(message.channel, '_'+trumps[random.randrange(0,5)]+'*_')

client.run(botkey)
