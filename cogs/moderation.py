import discord
import asyncio
import datetime
import time
from math import trunc
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.channel.send(f'''Successfully kicked {member.display_name} for the reason: `{reason}` ''')

        except Exception as e:
            await ctx.channel.send(f'''The user {member} could not be kicked. ''')

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.channel.send(f'''Successfully banned {member.display_name} for the reason: {reason} ''')

        except Exception as e:
            await ctx.channel.send(f'''The user {member} could not be banned. ''')

    #TODO: Add unban
    #TODO Add checks

    @commands.command()
    async def clear(self, ctx, limit):
        await ctx.channel.purge(limit=int(limit) + 1)
        await ctx.channel.send(f'''The last {limit} of messages have been cleared successfully!''')


def setup(client):
    client.add_cog(Moderation(client))
