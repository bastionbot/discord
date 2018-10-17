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
import sqlite3
import handler

corpus = [""]
client = discord.Client()
msg = {}
db = sqlite3.connect('bastion.db')

welcomeMsg1 = "> Welcome to Serious Overchill! "
welcomeMsg3 = "Check the pins here in <#193536175451930624> on how to get your very own vanity roles for pretty colors and "
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

class scheduleHandler(threading.Thread): #not working yet, everything is broken
    def __init__(self):
        threading.Thread.__init__(self)
        self.s = sched.scheduler(datetime.datetime, time.sleep)
        self.daemon = True
    def run(self):
        self.s.enterabs(datetime.datetime + datetime.timedelta(days=7), 2, markov.buildcorpus)
            
def start():
    os.chdir('/usr/local/bin/discord')
    s.enterabs(datetime.datetime + datetime.timedelta(days=7), 2, buildcorpus)
    corpus[0] = markov.buildcorpus()
    config = configparser.ConfigParser()
    config.read('config')
    with open('welcome') as f:
        welcomeMsgStrings = f.readlines()
    twitkeys = dict(config['twitter'])
    api = twitter.Api(**twitkeys)
    t = mentionHandler(api, str(config['standard']['oldMention']))
    t.start()
    s = scheduleHandler()
    s.start()
    return config, corpus, t, s, welcomeMsgStrings, api

@atexit.register
def stop():
    with open('config', 'w') as f:
        config.write(f)

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
    handler.writeCorpus(message, db)
    handler.message(message)

@client.event
async def on_member_join(member):
    msg = "<@" + str(member.id) + welcomeMsg1 + welcomeMsg3 \
    + welcomeMsg4 + welcomeMsg5 + markov.sayrandomshit(corpus[0], "foo") + "```"
    await client.send_message(client.get_channel(config['standard']['botchannel']), msg)

config, corpus, t, s, welcomeMsgStrings, api = start()
print('Corpus built')
print('------')
client.run(config['standard']['botkey'])
