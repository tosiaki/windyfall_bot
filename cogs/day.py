import discord
from discord.ext import commands
import datetime

from day_greeting import DayGreeting

day_words = {
        'morning': ['mornin', 'ohayo', '\'morn'],
        'afternoon': ['afternoon'],
        'evening': ['evenin', 'konbanwa'],
        'night': ['night', 'oyasumi'],
        'welcome': ['welcome']
        }

class Day(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        for word, names in day_words.items():
            for name in names:
                if name in message.content.lower():
                    if message.author.bot:
                        return
                    else:
                        self.add_resource(
                                message.author.id,
                                message.guild.id,
                                word
                                )

    def add_resource(self, user_id, guild_id, resource):
        time_delta = datetime.timedelta(hours=18)
        time_now = datetime.datetime.now()
        exists = self.client.session.query(DayGreeting.id) \
                .filter_by(
                        discord_user_id=user_id,
                        guild_id=guild_id,
                        type=resource
                        ) \
                .scalar() is not None

        if exists:
            query = self.client.session.query(DayGreeting) \
                    .filter_by(
                            discord_user_id=user_id,
                            guild_id=guild_id,
                            type=resource
                            )
            if time_now - query.first().latest > time_delta:
                query.update({
                    'count': DayGreeting.count+1
                    })
                self.client.session.commit()

        else:
            self.client.session.add(DayGreeting(
                count = 1,
                discord_user_id = user_id,
                guild_id = guild_id,
                type = resource
                ))
            self.client.session.commit()

    @commands.command()
    async def things(self, ctx):
        if ctx.author.bot:
            return
            
        session = self.client.session
        query = session.query(DayGreeting.type, DayGreeting.count).filter_by(
            discord_user_id = ctx.author.id,
            guild_id = ctx.guild.id
            )

        message = "```"
        for resource, count in query:
            message += f"{resource}: {count}\n"
        if message == "```":
            message+= "Nothing"
        message += "```"
        await ctx.send(message)

def setup(client):
    client.add_cog(Day(client))
