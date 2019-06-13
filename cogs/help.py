import discord
from discord.ext import commands
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.command()
    async def help(self, ctx):
        embeds = [
            discord.Embed(title="iBot - Help - Page 1", description=f"**Moderation commands**:\n **Kick**: Kicks a user from the server. Usage: {ctx.prefix}kick <user> <reason> \n **Ban**: Bans the user from rejoining the server. Usage: {ctx.prefix}ban <user> <reason>. \n **Mute**: Prevents the user from chatting. Usage: {ctx.prefix}mute <user> <reason>\n **Unban**: Removes the user from the banned user list. Usage: {ctx.prefix}unban <user> \n **Unmute**: Removes the muted status from the user. Usage: {ctx.prefix}unmute <user>", color=discord.Color.dark_purple()),
            discord.Embed(title="iBot - Help - Page 2", description=f"**Utility commands**:\n **Ping**: Checks the delay from the bot to the server. Usage: {ctx.prefix}ping", color=discord.Color.dark_purple())
            #TODO: Add more help categories and such.     
        ]
                
            
        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()


def setup(client):
    client.add_cog(Help(client))