import discord
import asyncio
import datetime
import time
from math import trunc
from discord.ext import commands

# These are some of the variables for the roles that can be used in some commands like kick and etc.
roles_can_kick = ['Admin', 'Mod', 'iApexx', 'Kick']
roles_can_ban = ['Admin', 'Mod', 'iApexx']
roles_can_mute = ['Admin', 'Mod', 'iApexx']
roles_can_clear = ['Admin', 'Mod', 'iApexx']


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_any_role(*roles_can_kick)
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
                     value=f'**User**: {member} [{member.id}]\n**Reason**: {reason}\n**Staff Member**: {ctx.message.author}')
        await self.client.get_channel(int(log_channel)).send(embed=em)
        # await self.punish("Kick", member, ctx.message.author, reason, 0) -- This is for when I will add the database

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send(f'''Error, you don't have permission to kick.''')
        elif isinstance(error, discord.HTTPException):
            await ctx.channel.send(f'''Error, kicking the user failed.''')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f'''Usage: {ctx.prefix}kick <user> <reason>''')

    @commands.command()
    async def ping(self, ctx):
        # The way the ping commands works is that it runs a timer, then sends a dummy message, then starts a new timer,
        current_time = time.perf_counter()
        await ctx.channel.send("") 
        time_after = time.perf_counter()

        await ctx.channel.purge(limit=1)

        final_time = time_after - current_time # Then it subtracts the before time from the time after the message,

        await ctx.channel.send(f'''Latancy is: `{round(final_time * 1000)}`ms''') # Then it rounds the number here.

    @commands.command()
    @commands.has_any_role(*roles_can_ban)
    async def ban(self, ctx, member : discord.Member, *, reason=None):

        if (reason == None): # We do this so that there is a different message sent to the user when a staff member has and has not specified a reason.
            await ctx.channel.send(f'''Successfully banned {member.display_name}''')
            message = f'''You have been banned from the server {member.guild.name}'''
            await member.send(message)
            await member.ban(reason=reason)
        else:
            await ctx.channel.send(f'''Successfully banned {member.display_name} for reason: {reason} ''')
            message = f'''You have been banned from the server {member.guild.name} for {reason}'''
            await member.send(message)
            await member.ban(reason=reason)

        log_channel = 422534466334883850 # This specifies the channel id where the log message will be sent TODO: Make it a variable!
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
    @commands.has_any_role(*roles_can_ban)
    async def unban(self, ctx, *, member, reason=None):
        banned_list = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        author = ctx.message.author
        # Runs a for loop where it loops through every member in the banned user list.
        for i in banned_list:
            user = i.user
            if (user.name, user.discriminator) == (member_name, member_discriminator): # If the member matches the user in the ban list, it will unban him.
                await ctx.guild.unban(user)
                await ctx.channel.send(f'''Successfully unbanned @{user.name}#{user.discriminator}!''')
                return

        try:
            await ctx.member.send(f'''You have been unbanned from the server!''') # Messages like these have to be in "try" since if it fails, it throws an error
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
    @commands.has_permissions(administrator=True)
    async def give(self, ctx, member : discord.Member, *, perm):
        role = discord.utils.get(ctx.guild.roles, name=perm) # This checks if the role the user specified exists.

        if perm is not 'kick' or 'ban' or 'mute' or 'clear': # This is just a safe guard so that users cannot give and make roles that are not meant to be made/given.
            await ctx.send(f"You haven't specified a valid permission. If you want help use {ctx.prefix}help give.")

        else:

            if role is None: # If a role does not exist, then it will create it.
                try:
                    role = await ctx.guild.create_role(name=perm, colour=discord.Color.light_grey())
                    await ctx.send(f'Creating the role {perm}!')
                except:
                    pass

            if perm == 'kick':
                await member.add_roles(role)
                await ctx.send(f'Giving the user {member.mention} permission to kick!')

            elif perm == 'ban':
                await member.add_roles(role)
                await ctx.send(f'Giving the user {member.mention} permission to ban!')

            elif perm == 'mute':
                await member.add_roles(role)
                await ctx.send(f'Giving the user {member.mention} permission to mute!')

            elif perm == 'clear':
                await member.add_roles(role)
                await ctx.send(f'Giving the user {member.mention} permission to clear the chat!')

            log_channel = 422534466334883850
            em = discord.Embed(color=discord.Color.dark_purple())
            em.set_footer().timestamp = datetime.datetime.utcnow()
            em.add_field(name='Give Permission', value=f'**User**: {member}\n**Responsible**: {ctx.message.author}\n**Permission**: {perm}')
            await self.client.get_channel(int(log_channel)).send(embed=em)

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f'''Usage: {ctx.prefix}give <user> <role>.''')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'''Error, you don't have permission to give permissions.''')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def revoke(self, ctx, member : discord.Member, *, perm):
        role = discord.utils.get(ctx.guild.roles, name=perm)

        if perm is not 'kick' or 'ban' or 'mute' or 'clear':
            await ctx.send(f"You haven't specified a valid permission. If you want help use {ctx.prefix}help revoke ")

        else:
            if perm == 'kick':
                await member.remove_roles(role)
                await ctx.send(f'Revoking the ability to kick from {member.mention}!')

            elif perm == 'ban':
                await member.remove_roles(role)
                await ctx.send(f'Revoking the ability to ban from {member.mention}!')

            elif perm == 'mute':
                await member.remove_roles(role)
                await ctx.send(f'Revoking the ability to mute from {member.mention}!')

            elif perm == 'clear':
                await member.remove_roles(role)
                await ctx.send(f'Revoking the ability to clear from {member.mention}!')

            log_channel = 422534466334883850
            em = discord.Embed(color=discord.Color.dark_purple())
            em.set_footer().timestamp = datetime.datetime.utcnow()
            em.add_field(name='Revoke Permission',
                         value=f'**User**: {member}\n**Responsible**: {ctx.message.author}\n**Permission**: {perm}')
            await self.client.get_channel(int(log_channel)).send(embed=em)

    @revoke.error
    async def revoke_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f'''Usage: {ctx.prefix}revoke <user> <role>.''')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'''Error, you don't have permission to revoke permissions.''')

    @commands.command()
    @commands.has_any_role(*roles_can_clear)
    async def clear(self, ctx, limit):
        await ctx.channel.purge(limit=int(limit) + 1)
        await ctx.channel.send(f'''The last {limit} of messages have been cleared successfully!''')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send("Error, you don't have permission to use clear!")


def setup(client):
    client.add_cog(Moderation(client))