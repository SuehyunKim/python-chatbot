import discord
from discord.ext import commands
import os

def main():
    prefix = '!'
    intents = discord.Intents.all()

    client = commands.Bot(command_prefix=prefix, intents = intents)

    @client.command(name='ping')
    async def _ping(ctx):
        await ctx.send('pong!')

    @client.command(name='이름')
    async def _name(ctx):
        name = ctx.message.author.display_name
        await ctx.send(f'Logged in as {name}')

    with open('token.txt', 'r') as f:
        token = f.read()

    client.run(token)

if __name__ == '__main__':
    main()