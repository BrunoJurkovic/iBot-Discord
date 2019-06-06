import discord
from discord.ext import commands
import time


class Log(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message, ctx):
        await self.channel.send(f'''The user {discord.Member.mention} has deleted a message, and the message was: "{message}"''')

def setup(client):
    client.add_cog(Log(client))


