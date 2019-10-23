from datetime import datetime
import asyncio

import bs4 as bs

async def ctx_print(_str, ctx=None):
    if ctx is not None:
        await ctx.send(_str)
    print(_str)

async def gofundme(url, ctx=None):
    await ctx_print(f"gofundme: {datetime.now().isoformat()}", ctx)
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
    await ctx_print(clean, ctx)

if __name__ == '__main__':
    asyncio.run(gofundme("https://www.gofundme.com/f/help-ben-finish-college"))
