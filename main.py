# We import the discord.py library to help us with the API calls and such
import discord

# This is the part of the code which reads the users token from a file names token.
def read_file():
    with open('token') as f:
        variable = f.read()

    return variable


private_token = read_file()

client = discord.Client()
client.run(private_token)
