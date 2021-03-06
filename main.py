# We import the discord.py library to help us with the API calls and such
import discord
import time
import asyncio
import os
from discord.ext import commands

client = commands.Bot(command_prefix=".")

logging_channel = ''
# This is the part of the code which reads the users token from a file names token.
def read_file():
    with open('token') as f:
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

private_token = read_file()
client.run(private_token) # This starts the bot
