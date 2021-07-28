import utils
from InfinityVoice import InfinityVoice,get_infinity_voice
from discord import Member,VoiceChannel
import discord.ext.commands as dcec
import asyncio
from collections import defaultdict

####config####
cog_modules = [
    "discord.Manager"
]

command_prefix = "v!"

####intialisation####

#create bot instance
bot = dcec.Bot(command_prefix,dcec.HelpCommand())
# bot = commands.Bot(command_prefix=command_prefix)

# for filename in os.listdir("./cogs"):
#     if filename.endswith(".py"):
#         bot.load_extension(f"cogs.{filename[:-3]}")

for module in cog_modules:
    bot.load_extension(module)

f = open("token.txt","r")
bot.run(f.read())
backup.saveAll(IV.infinityVoices)
