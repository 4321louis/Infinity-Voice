import discord
from discord.ext import commands
from InfinityVoice import InfinityVoice,get_infinity_voice

from datetime import datetime
from collections import defaultdict
from Utils import timestamp

from backup.TextJsonBackup import TextJsonBackup

class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Hashmap has guildId as key and list of InfinityVoices as value
        self.guildMap = defaultdict(list)

    #######################################
    ###############LISTENERS###############
    #######################################
    
    ####Static####

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        timestamp("Bot launched")
        print("Logged in as")
        print(self.bot.user.name, "id:", self.bot.user.id)
        print("------")
        self.guildMap = TextJsonBackup.loadAll()
        print(self.guildMap)

    @commands.Cog.listener()
    async def on_disconnect(self) -> None:
        timestamp("Bot disconnected")
        TextJsonBackup.saveAll(self.guildMap)
        timestamp("Saving: " + self.guildMap)


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
    #FIXME:fix this if statements logic
    #when an infinity voice channel is edited (but not by the bot) updates the references for channels in that infinity voice
        if before.name == after.name:
            await InfinityVoice.get_infinity_voice(before).reload_references()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.infinityVoices[guild.id] = []

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.infinityVoices.pop(guild.id)

    ####IV specific####

    @commands.Cog.listener()
    async def on_voice_state_update(member:Member, before, after):
        #update the infinity voice that was affected
        if (before.channel != None):
            await get_infinity_voice(before.channel).on_voice_state_update(member, before, after)
        if (after.channel != None):
            await get_infinity_voice(after.channel).on_voice_state_update(member, before, after)



    ######################################
    ###############COMMANDS###############
    ######################################

    ####static####

    #TODO:HELP? look into the help command in the library
    # @bot.command()
    # async def help(ctx,command)
    #     pass

    #TODO:think about what name_format is for the end user
    ##i.e. "Gaming {}" where {} is the number? how about special chars instead? which?

    # Create a new infinityVoice
    @commands.command()
    async def create(self, ctx, name_format: str, user_limit: int = 0) -> None:
        #TODO reactivate this if statement to restrict command to admin 
        # if ctx.message.author.guild_permissions.administrator:
        if True:
            print("New InfinityVoice creation request")
            print("Name format:", name_format)
            print("User limit:", user_limit)
            new = InfinityVoice(ctx.guild,name_format,int(user_limit))
            print("created an infinity voice")
            self.guildMap[ctx.guild.id].append(new)
            await new.on_size_change()

    ####IV specific####


    # TODO:Change this command to edit an entire IV only not specific channels
    # + add show and hide commands for editing specfic channels

    # Edit infinityVoice
    @commands.command()
    async def edit(self, ctx) -> None:
        # FIXME:get_infinity_voice location
        iv = InfinityVoice.get_infinity_voice(ctx.author.voice.channel)
        if iv == None: 
            ctx.send("Please join an Infinity Voice")
            return
        else:
            iv.edit()
        # FIXME:remove this \/
        if number == "list":
            await ctx.send(iv.overrides.toString())
        elif number.isnumeric():
            if not (int(number) in iv.overrides or number == "0"):
                print("Not implemented")
                #TODO sort out default channel override
                iv.overrides[int(number)] = ChannelSettings()
            iv.overrides[int(number)].editing = True

    # Save infinityVoice   
    @commands.command()
    async def save(self, ctx) -> None:
        # FIXME:get_infinity_voice location
        iv = InfinityVoice.get_infinity_voice(ctx.author.voice.channel)
        if iv == None: 
            ctx.send("Please join an Infinity Voice")
            return
        else:
            iv.save()
        # FIXME: remove the rest of this
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

    ####Temporary/Debug####
    @commands.command()
    #4321louis' panic button
    async def bleh(ctx):
        if ctx.message.author.id == 184599719060832257:
            IV.infinityVoices = {}

    @commands.command()
    #4321louis' other panic button
    async def saveall(ctx):
        if ctx.message.author.id == 184599719060832257:
            backup.saveAll(IV.infinityVoices)

    # @bot.command()
    # async def load(ctx, extension):
    #     bot.load_extension(f"cogs.{extension}")

    # @bot.command()
    # async def unload(ctx, extension):
    #     bot.unload_extension(f"cogs.{extension}")

 
    ################################

    # Returns the infinityvoice the given channel is in
    def get_infinity_voice(self,channel: VoiceChannel) -> Union[InfinityVoice, None]:
        for infinity_voice in infinityVoices[channel.guild.id]:
            for active_channel in infinity_voice.active_channels:
                if channel == active_channel:
                    return infinity_voice
        return None
        
    def setup(self,bot):
        bot.add_cog(Manager(bot))