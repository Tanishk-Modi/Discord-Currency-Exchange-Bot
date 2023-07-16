import discord
from discord.ext import commands
import requests

intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)

# Event triggered when the bot is ready and connected to Discord

@client.event
async def on_ready():
    print(f'{client.user} is running!')
    channel = client.get_channel()
    await channel.send("Hello, I am the finance bot. Type '$help' to learn more about me.")

# Custom help command class

class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        help_message = """
        To convert currencies, use the following command:
        `$convert <amount> <base_currency> <target_currency>`
        
        Example: `$convert 100 USD EUR`

        To gain insight about a particular stock, use the following command:
        `$stock <ticker symbol>`

        Example: `$stock AAPL`

        """
        await self.context.send(help_message)

client.help_command = CustomHelpCommand()


#Command to convert currencies

@client.command()
async def convert(ctx, amount: float, base: str, target: str):
    url = f'https://api.exchangerate-api.com/v4/latest/{base}'
    response = requests.get(url)
    data = response.json()

    if target.upper() in data['rates']:
        rate = data['rates'][target.upper()]
        converted_amount = amount * rate
        await ctx.send(f'{amount} {base.upper()} is equal to {converted_amount} {target.upper()}')
    else:
        await ctx.send(f"Sorry, I couldn't convert the currencies.")


# Command to retrieve stock information

@client.command()
async def stock(ctx, symbol: str):
    api_key = ''
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'Global Quote' in data:
        stock_symbol = data['Global Quote']['01. symbol']
        stock_open = data['Global Quote']['02. open']
        stock_high = data['Global Quote']['03. high']
        stock_low = data['Global Quote']['04. low']
        stock_price = data['Global Quote']['05. price']
        stock_volume = data['Global Quote']['06. volume']
        stock_previous_close = data['Global Quote']['08. previous close']

        message = f'Stock: {stock_symbol}\n'
        message += f'Open: {stock_open}\n'
        message += f'High: {stock_high}\n'
        message += f'Low: {stock_low}\n'
        message += f'Price: {stock_price}\n'
        message += f'Volume: {stock_volume}\n'
        message += f'Previous Close: {stock_previous_close}'

        await ctx.send(message)
    else:
        await ctx.send(f"Stock symbol {symbol} is not found.")


#Command that provides cryptocurrency data (bitcoin and ethereum)

@client.command()
async def crypto(ctx):
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()

    if 'bitcoin' in data and 'ethereum' in data:
        btc_price_usd = data['bitcoin']['usd']
        eth_price_usd = data['ethereum']['usd']
        
        message = f'Crypto Prices:\nBitcoin (USD): {btc_price_usd}\nEthereum (USD): {eth_price_usd}'
        await ctx.send(message)
    else:
        await ctx.send('Failed to fetch crypto prices.')


# This is the unique identifier for the bot
TOKEN = ''

client.run(TOKEN)

