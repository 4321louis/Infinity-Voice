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
        # {server: [infinityvoices]}
        self.infinityVoices = {}

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        utils.print_timed("")
        print("Logged in as")
        print(self.bot.user.name, "id:", self.bot.user.id)
        print("------")
        f = open("infinityVoiceSaves.txt", "r")
        self.infinityVoices = self.json_decoder(f.read())
        print(self.infinityVoices)
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        utils.print_timed("Disconnected")
        save_infinities(self)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before, after):
    #update the infinity voice that was affected

    # get infinityvoice from given channel, then update infinityvoice

        if (before.channel != None):
            # looping through infinityvoices in server
            (await get_infinity_voice(self, before.channel)).on_size_change()
            
            # for infinityvoice in self.infinityVoices[before.channel.guild_id]:
            #     for active_channel in infinityvoice.active_channels:
            #         if before.channel == active_channel:
            #             await infinityvoice.on_size_change()

        if (after.channel != None):
            # looping through infinityvoices in server

            (await get_infinity_voice(self, after.channel)).on_size_change()
            # for infinityvoice in self.infinityVoices[before.channel.guild_id]:
            #     for active_channel in infinityvoice.active_channels:
            #         if before.channel == active_channel:
            #             await infinityvoice.on_size_change()



            # await InfinityVoice.get_infinity_voice(before.channel).on_size_change()
        
            # await InfinityVoice.get_infinity_voice(after.channel).on_size_change()

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
    #TODO:fix this if statements logic
    #when an infinity voice channel is edited (but not by the bot) updates the references for channels in that infinity voice
        if before.name == after.name:
            await InfinityVoice.get_infinity_voice(before).reload_references()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.infinityVoices[guild.id] = []

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.infinityVoices.pop(guild.id)

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
                iv.overrides[int(number)] = utils.ChannelOverride()
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

    async def json_decoder(self, str:str) -> dict:
        loaded = json.loads(str)
        final = {}
        for str_guild_id,infinity_voice_ids in loaded.items():
            guild_id = int(str_guild_id)
            final[guild_id] = []
            for infinity_voice_dict in infinity_voice_ids:
                final[guild_id].append(InfinityVoice(bot.get_guild(infinity_voice_dict["guild"]),infinity_voice_dict["name_format"],infinity_voice_dict["user_limit"]))
                for channel_id in infinity_voice_dict["active_channels"]:
                    final[guild_id][-1].active_channels.append(bot.get_channel(channel_id))
                default_dict = infinity_voice_dict["overrides"]["null"]
                # TODO:kwargs please probs
                default = utils.ChannelOverride()
                default.name_format = default_dict["name_format"]
                default.limit = default_dict["limit"]
                default.overwrites = default_dict["overwrites"]
                default.category = bot.fetch_channel(default_dict["category"])
                default.position = default_dict["position"]
                final[guild_id][-1].overrides = defaultdict(default)
                for number in infinity_voice_dict["overrides"]:
                    if number == "null":continue
                    override_dict = infinity_voice_dict["overrides"][number]
                    # TODO:kwargs please probs
                    override = utils.ChannelOverride()
                    override.name_format = override_dict["name_format"]
                    override.limit = override_dict["limit"]
                    override.overwrites = override_dict["overwrites"]
                    override.category = bot.fetch_channel(override_dict["category"])
                    override.position = override_dict["position"]
                    final[guild_id][-1].overrides[int(number)] = override

        return final

async def get_infinity_voice(infinityvoicetool:InfinityVoiceTools, channel:discord.VoiceChannel) -> InfinityVoice:
    for infinity_voice in (await infinityvoicetool.infinityVoices)[channel.guild.id]:
        for active_channel in infinity_voice.active_channels:
            if channel == active_channel:
                return infinity_voice
    return None

def save_infinities(infinityvoicetool:InfinityVoiceTools):
    # save as dict{guild.id: [infinityvoices]}
    f = open("InfinityVoiceSaves.txt","w+")
    dump=json.dumps(infinityvoicetool.infinityVoices,default=json_encoder)
    utils.print_timed("Saving:"+ dump)
    f.write(dump)
    f.close()

def json_encoder(obj: object):
    if isinstance(obj,discord.Guild) or isinstance(obj,discord.VoiceChannel):
        return obj.id
    if isinstance(obj,InfinityVoice) or isinstance(obj,utils.ChannelOverride):
        return obj.__dict__


def setup(bot):
    bot.add_cog(InfinityVoiceTools(bot))