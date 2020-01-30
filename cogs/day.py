import discord
from discord.ext import commands
import datetime
from sqlalchemy.sql import exists, and_

from day_greeting import DayGreeting
from day_greeting import NewMemberJoin

day_words = {
        'morning': ['mornin', 'ohayo', '\'morn'],
        'afternoon': ['afternoon'],
        'evening': ['evenin', 'konbanwa'],
        'night': ['night', 'oyasumi'],
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

        if 'welcome' in message.content.lower():
            self.add_welcome(message.author.id, message.guild.id)

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

    def add_welcome(self, author_id, guild_id):
        exists = self.check_welcomes_exists(author_id, guild_id)
        start_time = self.get_welcome_start_time(exists, author_id, guild_id)
        welcomes = self.get_welcomes(guild_id, start_time)
        if exists:
            query = self.client.session.query(DayGreeting) \
                    .filter_by(
                            discord_user_id=author_id,
                            guild_id=guild_id,
                            type='welcome'
                            )
            query.update({ 'count': DayGreeting.count+welcomes})
            self.client.session.commit()
        else:
            self.client.session.add(DayGreeting(
                count = welcomes,
                discord_user_id = author_id,
                guild_id = guild_id,
                type = 'welcome'
                ))
            self.client.session.commit()

    def check_welcomes_exists(self, author_id, guild_id):
        return self.client.session.query(exists().where(and_(
            DayGreeting.discord_user_id==author_id,
            DayGreeting.guild_id==guild_id,
            DayGreeting.type=='welcome'
            ))).scalar() > 0

    def get_welcome_start_time(self, exists, author_id, guild_id):
        six_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=6)
        if exists:
            return max(self.client.session.query(DayGreeting).filter_by(
                    discord_user_id = author_id,
                    guild_id = guild_id,
                    type = 'welcome'
                    ).first().latest, six_hours_ago)
        else:
            return six_hours_ago

    def get_welcomes(self, guild_id, start_time):
        return self.client.session.query(NewMemberJoin).filter(and_(
                NewMemberJoin.guild_id == guild_id,
                NewMemberJoin.date > start_time
                )).count()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return

        self.client.session.add(NewMemberJoin(
            guild_id = member.guild.id
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
