import discord
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup


#import search_runpee # search class we will impelement later
my_secret = os.environ['token']
'''
# If you are coding the bot on a local machine, use the python-dotenv pakcage to get variables stored in .env file of your project
from dotenv import load_dotenv
load_dotenv()
'''


# instantiate discord client 
client = discord.Client()

# discord event to check when the bot is online 
@client.event
async def on_ready():
  print(f'{client.user} is now online!')

@client.event
async def on_message(message): 
  # make sure bot doesn't respond to it's own messages to avoid infinite loop
  if message.author == client.user:
      return  
  # lower case message
  message_content = message.content.lower()  
  
  if message.content.startswith(f'$earnings'):
    url_to_scrape = 'https://finance.yahoo.com/calendar/earnings'
    request_page = urlopen(url_to_scrape)
    page_html = request_page.read()
    request_page.close()
    html_soup = BeautifulSoup(page_html, 'html.parser')
    earnings_today = html_soup.find_all('a', {"data-test":"quoteLink"})
    for symbol in earnings_today:
      symbols = symbol.text.strip()
      await message.channel.send(symbols)

# get bot token from .env and run client
# has to be at the end of the file
client.run(my_secret)
