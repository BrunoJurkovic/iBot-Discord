import discord
from discord.ext import commands
import datetime


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log_channel = 422534466334883850

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):



        em = discord.Embed(description=f"**Message edited in {before.channel.mention}**",
                           colour=discord.Colour.dark_purple())
        em.set_author(name=before.author, icon_url=before.author.avatar_url)
        em.set_footer().timestamp = datetime.datetime.utcnow()
        em.add_field(name='Before', value=f'{before.content[:512]}{"..." if len(before.content) > 512 else ""}',
                     inline=False)
        em.add_field(name='After', value=f'{after.content[:512]}{"..." if len(after.content) > 512 else ""}\n​',
                     inline=False)
        try:
            await self.client.get_channel(int(self.log_channel)).send(embed=em)
        except:
            pass


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        attachments = '\r'
        if message.attachments != [] or message.embeds != []:
            for j in message.attachments:
                attachments += 'Attachment: ' + j.url + '\r\n'
            for j in message.embeds:
                attachments += 'Embed: ' + str(j.to_dict()) + '\r\n'
        em = discord.Embed(
            description=f'**Message sent by {message.author.mention} deleted in {message.channel.mention}**\n {message.content}\n​{attachments}\r\n',
            color= discord.Color.dark_purple())
        em.set_author(name=message.author, icon_url=message.author.avatar_url)
        em.set_footer().timestamp = datetime.datetime.utcnow()
        await self.client.get_channel(int(self.log_channel)).send(embed=em)

def setup(client):
    client.add_cog(Events(client))


