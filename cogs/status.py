import discord
from discord.ext import tasks, commands
from itertools import cycle


class Status(commands.Cog):
    def __init__(self, client):
        self.client = client


    game = cycle(['with the API', 'with scissors'])
    @tasks.loop(seconds=10)
    async def change_status(self, client, status= game):
        client.change_presence(activity=discord.Game(next(status)))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Bot ready")

def setup(client):
    client.add_cog(Status(client))