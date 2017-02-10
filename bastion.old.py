import discord
import asyncio
import markov
import sys
import random
import re

corpus = sys.argv[1]
client = discord.Client()
#react = re.compile(r'\bbot\b | \bomnic\b | \bbastion\b', flags=re.I | re.X)
trump = [ 'trump', 'Trump' ]
trumps = [ 'Orangegropenfuhrer', 'hate mango', 'cheeto golem', 'Hair Furor', 'trumpster fire' ]
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

#stalkme = ''
#stalked = 1
@client.event
async def on_message(message):
#	global stalkme
#	global stalked
#	if react.search(message.content):
#		if stalkme == message.author.id:
#			stalked += 1
#		else:
#			stalkme = message.author.id
#			stalked = 1
	msgcontent = message.content
	writecontent = msgcontent + '.\n'
	msgauthor = str (message.author)
	if not '274350023473496064' == message.author.id and not message.content.startswith('!') and not 'BroBot' in msgauthor:
		wfile = open("discord_corpus", "a")
		wfile.write(re.sub(r'<[@]?[&!]?[\d]*>','',writecontent))
		wfile.close()
#	sethrnd = random.randrange(1,5)
#	fuckseth = '<@'+message.author.id+'> ```' +markov.sayrandomshit('fuck_seth') + '```'
	if message.content.startswith('!markov'):
		msg = markov.sayrandomshit(corpus)
		tmp = await client.send_message(message.channel, msg)
	elif 'rad' in msgcontent:
		await client.send_message(client.get_channel('193536175451930624'), 'hell yeah')
	elif any(word in trump for word in msgcontent.split(" ")):
		await client.send_message(message.channel, '_'+trumps[random.randrange(0,5)]+'*_')
#	elif stalkme == message.author.id:
#		if sethrnd == 3:
#			await client.send_message(client.get_channel('193536175451930624'), fuckseth)
#			print(str(message.author) + ' has been sent ' + str(stalked) + ' messages.')



client.run('')
