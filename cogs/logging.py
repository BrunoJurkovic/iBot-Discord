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
        with open('users.json', 'r') as file:
            users = json.load(file)

        # do stuff

        with open('users.json', 'w') as file:
            json.dump(users, file)

    @commands.Cog.listener()
    async def on_message(self, message):

        with open('users.json', 'r') as file:
            users = json.load(file)


        # do other stuff

        with open('users.json', 'w') as file:
            json.dump(users, file)

def setup(client):
    client.add_cog(Logging(client))