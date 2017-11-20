import discord
import markov
import random
import re
import sys
import os
import twitter
import threading
import asyncore
import time
import configparser

corpus = [""]
client = discord.Client()
msg = {}

welcomeMsg1 = "> Welcome to Serious Overchill! "
welcomeMsg3 = " Check the pins here in <#193536175451930624> on how to get your very own vanity roles for pretty colors and "
welcomeMsg4 = "LFG pings. Stuck or have questions? Don\'t be afraid to ask a Kabalite or Mod in <#184804980794851328> for help! "
welcomeMsg5 = "Brace yourself for a Bastion Thought™: ```"

class mentionHandler(threading.Thread):
    def __init__(self, api, oldMention):
        threading.Thread.__init__(self)
        self.api = api
        self.oldMention = config['twitter']['oldMention']
        self.daemon = True
        self.respond = {}

    def run(self):
        global corpus
        while True:
            self.respond = {}
            time.sleep(300)
            mentions, replies = self.api.GetMentions(since_id=self.oldMention), self.api.GetReplies(since_id=self.oldMention)
            for line in mentions:
                if line.user.screen_name != "SRSOC_Bastion":
                    self.respond[line.id_str] = line.user.screen_name
            for line in replies:
                if line.user.screen_name != "SRSOC_Bastion":
                    self.respond[line.id_str] = line.user.screen_name
            if len(self.respond) is 0:
                continue
            self.oldMention = sorted(self.respond.keys())[-1]
			config['twitter']['oldMention'] = self.oldMention
            for i in self.respond.keys():
               self.api.PostUpdate(status="@"+self.respond[i]+" "+markov.sayrandomtweet(corpus[0]), in_reply_to_status_id=i)

t = mentionHandler(api, config['twitter']['oldMention'])
t.start()

def start():
	os.chdir('/usr/local/bin/discord')
	corpus[0] = markov.buildcorpus()
	config = configparser.ConfigParser()
	config.read('config')
	twitter = config['twitter']
    api = twitter.Api(**twitter)
	return api, config, corpus

def stop():
	with open('config', 'w') as f:
		config.write(f)

def writeCorpus(message, writecontent):
    writecontent = message.content + '\n'
    if message.author.id not in config['ignoreUsers'] and not message.content.startswith('!') and message.channel.id not in config['ignoreChannels']:
        with open("discord_corpus", "a") as wfile:
			wfile.write(re.sub(r'http\S+', '', re.sub(r'<[@]?[&!]?[\d]*>','',writecontent)))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(client.get_channel(config['botchannel']), 'Bastionbot restarted')

@client.event
async def on_message(message):
    global msg
	writeCorpus(message)
    if message.content.startswith('!tweet'):
        try:
            tweet = api.PostUpdate(msg[message.author.id])
            twitmsg = "https://twitter.com/SRSOC_Bastion/status/"+tweet.id_str
            await client.send_message(message.channel, twitmsg)
        except:
            await client.send_message(message.channel, 'Failed to tweet :saddowns:')
    if message.content.startswith('!markov'):
        try:
            msg[message.author.id] = markov.sayrandomshit(corpus[0])#, str(re.sub(r'!\w+\s', '', msgcontent)))
        except:
            msg[message.author.id] = 'Something bad happened and I don\'t know what'
        await client.send_message(message.channel, msg[message.author.id])
    if message.content.startswith('!update') and message.channel.id == config['DEFAULT']['adminchannel']:
        config['DEFAULT']['welcomeMsgStrings'].append(re.sub(r'!\w+\s', '', message.content))
        with open("welcome", "a") as wfile:
			wfile.write(re.sub(r'!\w+\s', '', message.content) + '\n')
        await client.send_message(message.channel, 'Successfully updated the welcome packet with ```' + re.sub(r'!\w+\s', '', message.content) + '```')
		
@client.event
async def on_member_join(member):
    msg = "<@" + str(member.id) + welcomeMsg1 + random.choice(welcomeMsgStrings).strip() + welcomeMsg3 \
    + welcomeMsg4 + welcomeMsg5 + markov.sayrandomshit(corpus[0]) + "```"
    await client.send_message(client.get_channel(config['DEFAULT']['welcomechannel']), msg)

print('Corpus built')
print('------')
start()
client.run(config['DEFAULT']['botkey'])
stop()