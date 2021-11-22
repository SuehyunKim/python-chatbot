import discord
from discord.ext import commands


class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("example Cog is Ready")

    @commands.command(name="임베드")
    async def embed(self, ctx):
        embed = discord.Embed(
            title='Embed의 제목입니다.',
            description='Embed 설명입니다.',
            color=discord.Color.blue())
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Example(client))
