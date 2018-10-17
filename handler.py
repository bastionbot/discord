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
