import discord
from discord.ext import commands
import requests

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

# Event triggered when the bot is ready and connected to Discord
@client.event
async def on_ready():
    print(f'{client.user} is running!')
    channel = client.get_channel(1118577601565429941)
    await channel.send("Hello, I am the currency exchange bot. Type '!help' to learn more about me.")

# Custom help command class
class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        help_message = """
        To convert currencies, use the following command:
        `!convert <amount> <base_currency> <target_currency>`
        
        Example: `!convert 100 USD EUR`

        """
        await self.context.send(help_message)

client.help_command = CustomHelpCommand()

#COmmand to convert currencies

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

# This is the unique identifier for the bot
TOKEN = ''

client.run(TOKEN)


