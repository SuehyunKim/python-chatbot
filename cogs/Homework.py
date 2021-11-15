from discord.ext import commands

class Homework(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Homework Cog is Ready")

    @commands.command(name="이름")
    async def _user(self, ctx):
        user = ctx.author.display_name
        await ctx.send(f'Logged in as {user}')

def setup(client):
    client.add_cog(Homework(client))