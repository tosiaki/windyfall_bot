import discord
from discord.ext import commands
from sqlalchemy.orm import sessionmaker

from testdata import TestData

Session = sessionmaker()

class TestCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        Session.configure(bind=client.engine)

    @commands.command()
    async def add_test_data(self, ctx, *, data):
        new_data = TestData(data=data)
        session = Session()
        session.add(new_data)
        session.commit()
        print(f"Added {data}.")

    @commands.command()
    async def get_test_data(self, ctx):
        session = Session()
        text = session.query(TestData).order_by(TestData.id.desc()).first().data
        await ctx.send(f"The data was {text}")

def setup(client):
    client.add_cog(TestCog(client))
