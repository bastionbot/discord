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

def message(message):
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
    return

def writeCorpus(message, db):
    if message.author.id in config['ignoreUsers']['users'].split(',\n'):
        return
    if message.content.startswith('!'):
        return
    if message.channel.id in config['ignoreChannels']['chans'].split(',\n'):
        return
    c = db.cursor()
    inputmessage = (message.timestamp, message.channel, message.author.id, message.content)
    c.execute("INSERT INTO chathistory VALUES (?,?,?,?)", inputmessage)
    return
