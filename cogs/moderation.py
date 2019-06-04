import discord
import asyncio
import time
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

def setup(client):
    client.add_cog(Moderation(client))
