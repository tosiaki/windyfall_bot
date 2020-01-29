import random
import os
import discord
from discord.ext import commands
import sqlalchemy
import psycopg2
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from get_random_quote import get_quote_with_conditions

load_dotenv()

client = commands.Bot(command_prefix = '.')

async def connect_to_db():
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_uri = f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}'
    client.engine = sqlalchemy.create_engine(db_uri)
    Session = sessionmaker(bind=client.engine)
    client.session = Session()

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain',
            'It is decidedly so.',
            'Without a doubt',
            'Yes―definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def motivation(ctx):
    quote = get_quote_with_conditions(lines=5, likes=10)
    with_markdown_quotes = quote["full_quote"].replace("\n", "\n> ")
    formatted_quote = f'> {with_markdown_quotes}'
    await ctx.send(f'{formatted_quote}\n―{quote["author_line"]}')

@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(f'Loaded {extension}')

@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(f'Unloaded {extension}')

@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'Reloaded {extension}')

client.loop.run_until_complete(connect_to_db())

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{os.path.splitext(filename)[0]}')

client.run(os.getenv("CLIENT"))
