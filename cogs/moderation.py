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
    async def kick(self, ctx, member: discord.Member, *, reason=None):

        if reason == None:
            message = 'You have been kicked from the server'
            try:
                await member.send(message)
            except:
                pass
            await ctx.channel.send(f'''Successfully kicked `{member.display_name}`''')
        else:
            message = 'You have been kicked from the server for ' + reason
            try:
                await member.send(message)
            except:
                pass
            await ctx.channel.send(f'''Successfully kicked {member.display_name} for `{reason}`''')


        await member.kick(reason=reason)

        log_channel = 422534466334883850
        em = discord.Embed(color=discord.Color.dark_purple())
        em.set_footer().timestamp = datetime.datetime.utcnow()
        em.add_field(name='Kick',
                     value=f'**User**: {member} [{member.id}]\n**Reason**: {reason}\n**Punisher**: {ctx.message.author}')
        await self.client.get_channel(int(log_channel)).send(embed=em)
        # await self.punish("Kick", member, ctx.message.author, reason, 0) -- This is for when I will add the database

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send(f'''Error, you don't have permission to ban.''')
        elif isinstance(error, discord.HTTPException):
            await ctx.channel.send(f'''Error, banning user failed.''')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f'''Usage: {ctx.prefix}kick <user> <reason>''')

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

        if (reason == None):
            await ctx.channel.send(f'''Successfully banned {member.display_name}''')
            message = f'''You have been banned from the server {member.guild.name}'''
            await member.send(message)
            await member.ban(reason=reason)
        else:
            await ctx.channel.send(f'''Successfully banned {member.display_name} for reason: {reason} ''')
            message = f'''You have been banned from the server {member.guild.name} for {reason}'''
            await member.send(message)
            await member.ban(reason=reason)

        log_channel = 422534466334883850
        em = discord.Embed(color=discord.Color.dark_purple())
        em.set_footer().timestamp = datetime.datetime.utcnow()
        em.add_field(name='Ban',
                    value=f'**User**: {member} [{member.id}]\n**Reason**: {reason}\n**Punisher**: {ctx.message.author}')
        await self.client.get_channel(int(log_channel)).send(embed=em)
        # await self.punish("Ban", member, ctx.message.author, reason, 0) -- This is for when I will add the database

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send(f'''Error, you don't have permission to ban.''')
        elif isinstance(error, discord.HTTPException):
            await ctx.channel.send(f'''Error, banning user failed.''')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f'''Usage: {ctx.prefix}ban <user> <reason>.''')

    @commands.command()
    async def unban(self, ctx, *, member, reason=None):
        banned_list = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        author = ctx.message.author
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
        em.add_field(name='Unban', value=f'**User**: {user.user}\n**Reason**: {reason}\n**Responsible**: {author}')
        await self.client.get_channel(int(log_channel)).send(embed=em)
        # await self.punish("UnBan", member, ctx.message.author, reason, 0) -- This is for when I will add the database

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send(f'''Error, you don't have permission to unban.''')
        elif isinstance(error, discord.HTTPException):
            await ctx.channel.send(f'''Error, unbanning user failed.''')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f'''Usage: {ctx.prefix}unban <user> <reason>.''')


    @commands.command()
    async def clear(self, ctx, limit):
        await ctx.channel.purge(limit=int(limit) + 1)
        await ctx.channel.send(f'''The last {limit} of messages have been cleared successfully!''')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send("Error, you don't have permission to use clear!")


def setup(client):
    client.add_cog(Moderation(client))