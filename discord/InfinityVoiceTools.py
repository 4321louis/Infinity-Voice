import discord
from discord.ext import commands

import utils
import asyncio
import bot
from collections import defaultdict
import json

# imports the class
from InfinityVoice import InfinityVoice

class InfinityVoiceTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Commands
    @commands.command()
    async def create(self, ctx, name_format, user_limit=0):
        #TODO if ctx.message.author.guild_permissions.administrator:
        if True:
            print("Name format:", name_format)
            print("User limit:", user_limit)
            new = InfinityVoice(ctx.guild,name_format,int(user_limit))
            
            if (not self.infinityVoices):
                (await self.infinityVoices)[ctx.guild.id].append(new)
            else:
                (await self.infinityVoices)[ctx.guild.id] = [new]
            print("created an infinity voice")
            await new.on_size_change()

    @commands.command()
    async def edit(self, ctx, number = "0"):
        iv = InfinityVoice.get_infinity_voice(ctx.author.voice.channel)
        if iv == None: 
            ctx.send("Please join an Infinity Voice")
            return
        if number == "list":
            await ctx.send(iv.overrides.toString())
        elif number.isnumeric():
            if not (int(number) in iv.overrides or number == "0"):
                iv.overrides[int(number)] = utils.ChannelSettings()
            iv.overrides[int(number)].editing = True

    @commands.command()
    async def save(self, ctx, number = "0"):
        iv = InfinityVoice.get_infinity_voice(ctx.author.voice.channel)
        if iv == None: 
            ctx.send("Please join an Infinity Voice")
            return
        if number == "all":
            for i in iv.overrides.keys().append("0"): 
                iv.overrides[i].editing = False
        if (int(number) in iv.overrides or number == "0"):
            if iv.overrides(int(number)).editing:
                iv.overrides[int(number)].editing = False
                if number == "0":
                    ctx.send("Saved default channel")
                else:
                    ctx.send("Saved channel " + str(number))
            else:
                ctx.send("That channel is not currently being edited")

    @commands.command()
    #4321louis' panic button
    async def bleh(self, ctx):
        if ctx.message.author.id == 184599719060832257:
            self.infinityVoices = {}

    @commands.command()
    #4321louis' other panic button
    async def saveall(self, ctx):
        if ctx.message.author.id == 184599719060832257:
            InfinityVoice.save_infinities()

def setup(bot):
    bot.add_cog(InfinityVoiceTools(bot))