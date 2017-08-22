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

os.chdir('/usr/local/bin/discord')
with open('twitkeys') as f:
    lines = f.readlines()
api = twitter.Api(consumer_key=lines[0].strip(), 
                  consumer_secret=lines[1].strip(),
                  access_token_key=lines[2].strip(),
                  access_token_secret=lines[3].strip())
with open('oldMention') as f:
    oldMention = f.readlines()[0].strip()
f = open("botkey", 'r')
botkey = str(f.readline())
f.close()
corpus = [""]
botkey = botkey.rstrip()
client = discord.Client()
msg = {}

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
            with open("oldMention") as f:
                self.oldMention = f.readlines()[0].strip()
            time.sleep(300)
            mentions = self.api.GetMentions(since_id=self.oldMention)
            replies = self.api.GetReplies(since_id=self.oldMention)
            for line in mentions:
                if line.user.screen_name != "SRSOC_Bastion":
                    self.respond[line.id_str] = line.user.screen_name
            for line in replies:
                if line.user.screen_name != "SRSOC_Bastion":
                    self.respond[line.id_str] = line.user.screen_name
            if len(self.respond) is 0:
                continue
            self.oldMention = sorted(self.respond.keys())[-1]
            wfile = open("oldMention", "w")
            wfile.write(self.oldMention)
            wfile.close()
            for i in self.respond.keys():
               self.api.PostUpdate(status="@"+self.respond[i]+" "+markov.sayrandomtweet(corpus[0]), in_reply_to_status_id=i)
        
t = mentionHandler(api, oldMention)
t.start()
                     
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
    global msg
    msgcontent = message.content
    writecontent = msgcontent + '\n'
    msgauthor = str(message.author)
    if not '274350023473496064' == message.author.id and not message.content.startswith('!') and 'BroBot' not in msgauthor:
        wfile = open("discord_corpus", "a")
        wfile.write(re.sub(r'<[@]?[&!]?[\d]*>','',writecontent))
        wfile.close()
    if message.content.startswith('!tweet'):
        try:
            tweet = api.PostUpdate(msg[message.author.id])
            twitmsg = "https://twitter.com/SRSOC_Bastion/status/"+tweet.id_str
            await client.send_message(message.channel, twitmsg)
        except:
            await client.send_message(message.channel, 'Failed to tweet :saddowns:')
    if message.content.startswith('!markov'):
        try:
            msg[message.author.id] = markov.sayrandomshit(corpus[0])
        except:
            msg[message.author.id] = 'Something bad happened and I don\'t know what'
        await client.send_message(message.channel, msg[message.author.id])

client.run(botkey)
