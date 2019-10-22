import threading
import datetime

from discord.ext.commands import Cog, command, group
import bs4 as bs

class PerpetualTimer():

    def __init__(self, t,hFunction,name):
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
    print(clean)


class Track(Cog):

    def _get_tracking_threads(self):
        return threading.enumerate()[:1]

    @group()
    async def track(self, ctx):
        """
        Gofundme tracking commands
        """
        if ctx.invoked_subcommand is not None:
            return
        await ctx.send(f'Command not found. Type `@{self.bot.user} help track` for a list of commands.')

    @track.command()
    async def stop(self, ctx, name):
        """
        Stops an active tracking by name.
        See the list command for a list of currently active tracking.
        """
        threads = {thread.name: thread for thread in self._get_tracking_threads()}
        thread = threads.get(name)
        if thread:
            thread.cancel()
            await ctx.send(f"Tracking of {name} stopped successfully.")
            return
        await ctx.send(
            f"Tracking by the name of {name} not found. Did you spell the name correctly?"
            f"Type `@{self.bot.user} track list` for a list of active tracking"
        )

    @track.command()
    async def list(self, ctx):
        """
        List currently tracked gofundmes.
        """
        threads = [f'{i}) {thread.name}' for i, thread in enumerate(self._get_tracking_threads(), 1)]
        await ctx.send('I\'m currently tracking the following GoFundMe pages!\n >>> '+ '\n'.join(threads))

    @track.command()
    async def start(self, ctx, url):
        """
        Give the bot a URL to track a gofundme!
        E.g. @Bastion track start https://www.gofundme.com/f/help-ben-finish-college
        Bastion will keep tabs on the latest contributors and announce progress milestones.
        """
        name = url.split('/')[-1]
        # We probably want to add validation to the URL...
        t = PerpetualTimer(60.0, gofundme, name, url)
        t.start()


def setup(bot):
    bot.add_cog(Track())
