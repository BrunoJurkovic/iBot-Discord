# We import the discord.py library to help us with the API calls and such
import discord
import time
import asyncio
import os
from discord.ext import commands
import asyncpg
import json

client = commands.Bot(command_prefix=".")

with open('dbinfo.json', 'r') as f:
    dbinfo = json.load(f)

async def create_db_connection():
    client.pg_connect = await asyncpg.connect(user=dbinfo['username'], password=dbinfo['password'], host=dbinfo['server'], port=dbinfo['port'], database=dbinfo['database'])

async def create_db_pool():
    client.pg_pool = await asyncpg.create_pool(database=dbinfo['database'], user=dbinfo['username'], password=dbinfo['password'])

# This is the part of the code which reads the users token from a file names token.
def read_file():
    with open('token.txt') as f:
        variable = f.read()

    return variable


#This will load the desired cogs
@client.command()
async def load(ctx, extension):
    try:
        client.load_extension(f'''cogs.{extension}''')
        await ctx.channel.send(f'''Successfully loaded {extension}''')
    except Exception as e:
        await ctx.channel.send(f'''Error! We could not load the extension {extension} because {e}''')

#This unloads the desired cogs
@client.command()
async def unload(ctx, extension):
    try:
        client.unload_extension(f'''cogs.{extension}''')
        await ctx.channel.send(f'''Successfully unloaded {extension}''')

    except Exception as e:
        await ctx.channel.send(f'''Error! We could not unload the extension {extension} because {e}''')

@client.command()
async def reload(ctx, extension):
    if extension == 'all':
        try:
            for file in os.listdir('./cogs'):
                if file.endswith('.py'):
                    client.reload_extension(f"""cogs.{file[:-3]}""")
            await ctx.channel.send(f'''Successfully reloaded all cogs!''')

        except Exception as e:
            await ctx.channel.send(f'''Error! We could not reload all cogs because "{e}"''')
    else:
        try:
            client.reload_extension(f'''cogs.{extension}''')
            await ctx.channel.send(f'''Successfully reloaded {extension}.''')

        except Exception as e:
            await ctx.channel.send(f'''Error! We could not reload the extension {extension} because "{e}"''')

# This checks every file in the cogs folder, and loads it
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f"""cogs.{file[:-3]}""") # this removes the .py extension from the filename


client.loop.run_until_complete(create_db_connection())
private_token = read_file()
client.run(private_token) # This starts the bot
