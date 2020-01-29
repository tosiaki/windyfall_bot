import discord
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cogtest(self, ctx):
        await ctx.send('This is a test cog command.')

def setup(client):
    client.add_cog(Example(client))
