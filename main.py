import discord
from discord.ext import commands
import os

def main():
    prefix = '!'
    intents = discord.Intents.all()

    client = commands.Bot(command_prefix=prefix, intents = intents)

    with open('token.txt', 'r') as f:
        token = f.read()

    client.run(token)

if __name__ == '__main__':
    main()