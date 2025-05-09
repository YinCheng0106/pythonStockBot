import discord, asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '>', intents = intents)

@client.event
async def on_ready():
    slash = await client.tree.sync()
    print(f'We have logged in as {client.user}')
    print(f"Synced {len(slash)} commands")

async def load_commands():
    for filename in os.listdir('./src/commands'):
        if filename.endswith('.py'):
            await client.load_extension(f'src.commands.{filename[:-3]}')


async def main():
    async with client:
        await load_commands()
        await client.start(os.getenv('bot_token'))

if __name__ == '__main__':
    asyncio.run(main())