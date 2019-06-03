# We import the discord.py library to help us with the API calls and such
import discord
# This is the part of the code which reads the users token from a file names token.
def read_file():
    with open('token') as f:
        variable = f.read()

    return variable


private_token = read_file()

client = discord.Client()

# This is dedicated to greeting users
@client.event
async def on_user_join(member):
    # TODO: Make users be able to pick their own channels
    greet_channel = ['welcome'] # This makes it so that users can only be greeted in the right channel
    if str(member.guild.channel) in greet_channel:
        await greet_channel.send(f"""Thank you to user {member.mention} for joining this server!""")


@client.event
async def on_message(msg):
    server_id = client.get_guild(422531871314935810)
    channels = ['commands', 'staff']
    #Checks if the user sends help, in which we return the help menu
    # TODO: Implement the help message
    if str(msg.channel) in channels:
        if msg.content.find('!!help') != -1:
            await msg.channel.send('Hey, this is not implemented yet.')

        elif msg.content == '!!members':
            await msg.channel.send(f"""There are {server_id.member_count} members in this Discord server.""")



client.run(private_token)