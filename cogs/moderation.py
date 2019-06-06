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
        await member.kick(reason=reason)
        await ctx.channel.send(f'''Successfully kicked {member.display_name} for the reason: `{reason}` ''')

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.channel.send(f'''Successfully banned {member.display_name} for the reason: {reason} ''')

    #TODO: Add unban
    # async def unban(self, ctx, user, *,  reason=None): BRUNO IDK HOW TO DO IT CURRENTLY

    @commands.command()
    async def ping(self, ctx): # ik it's bad code
        current_time = time.perf_counter()
        await ctx.channel.send("")
        time_after = time.perf_counter()

        await ctx.channel.purge(limit=1)

        final_time = time_after - current_time

        await ctx.channel.send(f'''Latancy is: `{round(final_time * 1000)}`ms''')

def setup(client):
    client.add_cog(Moderation(client))
