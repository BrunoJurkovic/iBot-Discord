import discord
import asyncio
import time
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

    #TODO: Add unban

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send(f'''The ping is `{round(self.client.latency * 1000)}` ms!''')


def setup(client):
    client.add_cog(Moderation(client))
