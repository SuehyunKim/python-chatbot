import discord
from discord.ext import commands
import os


def main():
    prefix = '!'
    intents = discord.Intents.all()

    client = commands.Bot(command_prefix=prefix,
                          intents=intents, help_command=None)

    for filename in os.listdir('./cogs'):
        if '.py' in filename:
            filename = filename.replace('.py', '')
            client.load_extension(f"cogs.{filename}")

    with open('token.txt', 'r') as f:
        token = f.read()

    @client.event
    async def on_member_join(member):
        if member.dm_channel:
            channel = member.dm_channel
        else:
            channel = await member.create_dm()
        name = member.name
        await channel.send(f'{name}님, 환영합니다!')

    @client.command(name="추가")
    async def _load(ctx, extension):
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension}이 추가되었어요!")

    @client.command(name="제거")
    async def _unload(ctx, extension):
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension}이 제거되었어요!")

    @client.command(name="새로고침")
    async def _reload(ctx, extension):
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension}이 새로고침되었어요!")

    client.run(token)


if __name__ == '__main__':
    main()
