# FIXME: this should be moved into manager for now as its just printing a string
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command()
    async def send_help(self, ctx):
        # send help embed
        # TODO:Help commands
        await ctx.send("this helps yeah?")

def setup(bot):
    bot.add_cog(Help(bot))