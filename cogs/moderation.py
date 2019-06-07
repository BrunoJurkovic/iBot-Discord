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

        if reason == None:
            reason = 'None'
            message = 'You have been kicked from the server for '
            if reason != 'None':
               try:
                message += reason
                await member.send(message)
               except:
                   pass

            else:
                try:
                 await member.send(message)
                except: pass
        try:
            await member.kick(reason=reason)
            await ctx.channel.send(f'''Successfully kicked {member.display_name} for the reason: `{reason}` ''')

        except Exception as e:
            await ctx.channel.send(f'''The user {member} could not be kicked. ''')

        log_channel = 422534466334883850
        em = discord.Embed(color=discord.Color.dark_purple())
        em.set_footer().timestamp = datetime.datetime.utcnow()
        em.add_field(name='Kick',
                     value=f'**User**: {member} [{member.id}]\n**Reason**: {reason}\n**Punisher**: {ctx.message.author}')
        await self.client.get_channel(int(log_channel)).send(embed=em)
        #await self.punish("Kick", member, ctx.message.author, reason, 0) -- This is for when I will add the database

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):

        if not reason:
            reason = 'None'
            message = 'You have been banned from the server for '
            if reason != 'None':
                message += reason
                await member.send(message)

            else:
                await member.send(message)

        try:
            await member.ban(reason=reason)
            await ctx.channel.send(f'''Successfully banned {member.display_name} for the reason: {reason} ''')

        except Exception as e:
            await ctx.channel.send(f'''The user {member} could not be banned. ''')

 
    @commands.command()
    async def ping(self, ctx): # ik it's bad code
        current_time = time.perf_counter()
        await ctx.channel.send("")
        time_after = time.perf_counter()

        await ctx.channel.purge(limit=1)

        final_time = time_after - current_time

        await ctx.channel.send(f'''Latancy is: `{round(final_time * 1000)}`ms''')
        
    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):

        if not reason:
            reason = 'None'
            message = 'You have been banned from the server for '
            if reason != 'None':
                message += reason
                await member.send(message)

            else:
                await member.send(message)

        try:
            await member.ban(reason=reason)
            await ctx.channel.send(f'''Successfully banned {member.display_name} for the reason: {reason} ''')

        except Exception as e:
            await ctx.channel.send(f'''The user {member} could not be banned. ''')

        log_channel = 422534466334883850
        em = discord.Embed(color=discord.Color.dark_purple())
        em.set_footer().timestamp = datetime.datetime.utcnow()
        em.add_field(name='Ban',
                     value=f'**User**: {member} [{member.id}]\n**Reason**: {reason}\n**Punisher**: {ctx.message.author}')
        await self.client.get_channel(int(log_channel)).send(embed=em)
        # await self.punish("Ban", member, ctx.message.author, reason, 0) -- This is for when I will add the database

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_list = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for i in banned_list:
            user = i.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f'''Successfully unbanned @{user.name}#{user.discriminator}!''')
                return

        try:
            await ctx.member.send(f'''You have been unbanned from the server!''')
        except:
            pass
        log_channel = 422534466334883850
        em = discord.Embed(color=discord.Color.dark_purple())
        em.set_footer().timestamp = datetime.datetime.utcnow()
        em.add_field(name='Unban',
                     value=f'**User**: {member} [{member.id}]\n**Staff Member**: {ctx.message.author}')
        await self.client.get_channel(int(log_channel)).send(embed=em)
        # await self.punish("UnBan", member, ctx.message.author, reason, 0) -- This is for when I will add the database

    #TODO Add checks

    @commands.command()
    async def clear(self, ctx, limit):
        await ctx.channel.purge(limit=int(limit) + 1)
        await ctx.channel.send(f'''The last {limit} of messages have been cleared successfully!''')



def setup(client):
    client.add_cog(Moderation(client))
