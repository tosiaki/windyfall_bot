import discord
from discord.ext import commands

class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author==159985870458322944:
            if 'level 5!' in message.content:
                user = message.mentions[0].id
                role_name = "Level ≧ 5"
                role = get(message.guild.roles, name=role_name)
                await self.client.add_roles(user, role)

def setup(client):
    client.add_cog(Levels(client))
