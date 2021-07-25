import discord
from discord.ext import commands
from InfinityVoice import InfinityVoice,get_infinity_voice

from datetime import datetime
from collections import defaultdict

from backup.TextJsonBackup import TextJsonBackup

class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Hashmap has guildId as key and list of InfinityVoices as value
        self.guildMap = defaultdict(list)

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
        timestamp("Bot shut off")
        TextJsonBackup.saveAll(self.guildMap)
        timestamp("Saving: " + self.guildMap)

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
            await new.on_size_change()

    # Edit infinityVoice
    @commands.command()
    async def edit(self, ctx, number: str = "0") -> None:
        iv = InfinityVoice.get_infinity_voice(ctx.author.voice.channel)
        if iv == None: 
            ctx.send("Please join an Infinity Voice")
            return
        if number == "list":
            await ctx.send(iv.overrides.toString())
        elif number.isnumeric():
            if not (int(number) in iv.overrides or number == "0"):
                print("Not implemented")
                #TODO sort out default channel override
                # iv.overrides[int(number)] = utils.ChannelOverride()
            iv.overrides[int(number)].editing = True

    # Save infinityVoice   
    @commands.command()
    async def save(self, ctx, number: str = "0") -> None:
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
        

def timestamp(message: str) -> None:
    print("[" + str(datetime.now()) + "]", message)

def setup(bot):
    bot.add_cog(Manager(bot))