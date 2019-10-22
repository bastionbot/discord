import threading, datetime
import bs4 as bs

class perpetualTimer():

	def __init__(self,t,hFunction,name):
		self.t=t
		self._name=name
		self.hFunction = hFunction
		self.thread = threading.Timer(self.t,self.handle_function)

	def handle_function(self):
		self.hFunction()
		self.thread = threading.Timer(self.t,self.handle_function)
		self.thread.start()

	def start(self):
		self.thread.start()

	def cancel(self):
		self.thread.cancel()
	
def gofundme(url):
	if url.split(' ')[-1:].startswith('http'):
		html = bs(urllib.request.urlopen(url.split(' ')[-1:]))
    donations = []
	name = html.find('h1').text
    progress = ''.join([x.text for x in html.find_all('h2',{'class':'m-progress-meter-heading'})])
    percent = list(progress.split(' ')[i].strip('$') for i in [0, 3])
    percentage = float('%.3f' %(int(percent[0].replace(',','')) / int(percent[1].replace(',','')) * 100))
    for ultag in html.find_all('ul', {'class': 'o-campaign-sidebar-donations'}):
	for litag in ultag.find_all('li'):
		donations.append(litag.text)
    clean = {x[0]: x[1] for x in [don.split('\xa0') for don in donations] if len(x) ==3}

@command()
async def track(self, ctx, *, command):
    """
    Give the bot a URL to track a gofundme! E.g. @ bastion track https://www.gofundme.com/f/help-ben-finish-college start
    Bastion will keep tabs on the latest contributors and announce progress milestones
    List currently tracked gofundmes with @ bastion track list
    Stop tracking a gofundme with @ bastion track # stop
    """
	cmd = command.split(' ')
	if cmd[-1] == 'stop':
		stop(cmd[-2])
	elif cmd[-1] == 'list':
		list()
	elif cmd[-1] == 'start':
		t = perpetualTimer(60.0,gofundme,[cmd[-2]],cmd[-2].split(' ')[2].split('/')[-1])
		t.start()
	else:
		await ctx.send(f'Command not found. Type `@{self.bot.user} help track` for a list of commands.')
	
	def stop(name):
		threads = threading.enumerate()[1:]
		for i in range(len(threads)):
			if name in str(threads[i]):
				threads[i].cancel()
	def list():
		threads = ['{}. {}'.format(i,x._name) for i,x in enumerate(threading.enumerate()[1:],1)]
		await ctx.send('I\'m currently tracking the following GoFundMe pages!\n >>> '+ '\n'.join(threads))
