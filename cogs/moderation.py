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

    @commands.command()
    async def ping(self, ctx): # ik it's bad code
        sent_time = ctx.message.created_at
        sec_time = (sent_time-datetime.datetime(1970,1,1)).total_seconds()
        current_time = time.time()

        # print(f'''{current_time} CURRENT TIME AFTER MSG''')
        # print(f'''{sec_time} TIME MESSAGE SENT''')

        final_time = current_time - sec_time
        await ctx.channel.send(f'''Ping is: `{trunc(final_time * 1000)}`ms''')

def setup(client):
    client.add_cog(Moderation(client))
