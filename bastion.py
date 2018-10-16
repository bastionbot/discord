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
import atexit

corpus = [""]
client = discord.Client()
msg = {}

welcomeMsg1 = "> Welcome to Serious Overchill! "
welcomeMsg3 = " Check the pins here in <#193536175451930624> on how to get your very own vanity roles for pretty colors and "
welcomeMsg4 = "LFG pings. Stuck or have questions? Don\'t be afraid to ask a Mod in <#184804980794851328> for help! "
welcomeMsg5 = "Brace yourself for a Bastion Thought™: ```"

class mentionHandler(threading.Thread):
    def __init__(self, api, oldMention):
        threading.Thread.__init__(self)
        self.api = api
        self.oldMention = oldMention
        self.daemon = True
        self.respond = {}

    def run(self):
        global corpus
        while True:
            self.respond = {}
            time.sleep(300)
            mentions, replies = self.api.GetMentions(since_id=self.oldMention), self.api.GetReplies(since_id=int(self.oldMention))
            for line in mentions:
                if line.user.screen_name != "SRSOC_Bastion":
                    self.respond[line.id_str] = line.user.screen_name
            for line in replies:
                if line.user.screen_name != "SRSOC_Bastion":
                    self.respond[line.id_str] = line.user.screen_name
            if len(self.respond) is 0:
                continue
            self.oldMention = sorted(self.respond.keys())[-1]
            config['standard']['oldMention'] = self.oldMention
            for i in self.respond.keys():
               self.api.PostUpdate(status="@"+self.respond[i]+" "+markov.sayrandomtweet(corpus[0]), in_reply_to_status_id=i)

def start():
    os.chdir('/usr/local/bin/discord')
    corpus[0] = markov.buildcorpus()
    config = configparser.ConfigParser()
    config.read('config')
    with open('welcome') as f:
        welcomeMsgStrings = f.readlines()
    twitkeys = dict(config['twitter'])
    api = twitter.Api(**twitkeys)
    t = mentionHandler(api, str(config['standard']['oldMention']))
    t.start()
    return config, corpus, t, welcomeMsgStrings, api

@atexit.register
def stop():
    with open('config', 'w') as f:
        config.write(f)

def writeCorpus(message):
    writeContent = message.content + '\n'
    if message.author.id in config['ignoreUsers']['users'].split(',\n'):
        return
    if message.content.startswith('!'):
        return
    if message.channel.id in config['ignoreChannels']['chans'].split(',\n'):
        return
    with open("discord_corpus", "a") as wfile:
        removeLinks = re.sub(r'http\S+', '', writeContent)
        removeMentions = re.sub(r'<[@]?[&!]?[\d]*>','', removeLinks)
        wfile.write(removeMentions)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(client.get_channel(config['standard']['botchannel']), 'Bastionbot restarted')

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
            msg[message.author.id] = markov.sayrandomshit(corpus[0], message.content)#, str(re.sub(r'!\w+\s', '', msgcontent)))
        except:
            msg[message.author.id] = 'Something bad happened and I don\'t know what'
        await client.send_message(message.channel, msg[message.author.id])
    if message.content.startswith('!update') and message.channel.id == config['standard']['adminchannel']:
        welcomeMsgStrings.append(re.sub(r'!\w+\s', '', message.content))
        with open("welcome", "a") as wfile:
            wfile.write(re.sub(r'!\w+\s', '', message.content) + '\n')
        await client.send_message(message.channel, 'Successfully updated the welcome lines with ```' + re.sub(r'!\w+\s', '', message.content) + '```')
    if message.content.startswith('!list') and message.channel.id == config['standard']['adminchannel']:
        tempmsg = ""
        for welcome in welcomeMsgStrings:
            tempmsg += welcome
        await client.send_message(message.channel, "Current welcome strings:\n"+"```"+tempmsg+"```")
    if message.content.startswith('!bruce') and message.channel.id == config['standard']['adminchannel']:
        try:
            server = client.get_server('184804980794851328')
           # print(server.get_member(message.content.split(' ')[1]).nick)
            client.change_nickname(server.get_member(message.content.split(' ')[1]), 'Bruce')
            await client.send_message(message.channel, message.author.mention + " you've bruced " + server.get_member(message.content.split(" ")[1]).nick)
        except:
            await client.send_message(message.channel, message.author.mention + " No dice, friend")

@client.event
async def on_member_join(member):
    msg = "<@" + str(member.id) + welcomeMsg1 + random.choice(welcomeMsgStrings).strip() + welcomeMsg3 \
    + welcomeMsg4 + welcomeMsg5 + markov.sayrandomshit(corpus[0], "foo") + "```"
    await client.send_message(client.get_channel(config['standard']['botchannel']), msg)

config, corpus, t, welcomeMsgStrings, api = start()
print('Corpus built')
print('------')
client.run(config['standard']['botkey'])
