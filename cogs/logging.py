import discord
from discord.ext import commands
import json
import time
import os

class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_user_join(self, user):
        print()

    @commands.Cog.listener()
    async def on_message(self, message):
        print()
def setup(client):
    client.add_cog(Logging(client))