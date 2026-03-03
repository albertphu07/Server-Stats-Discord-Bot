import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

#discord bot token
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

#Log (This is going to make my disk full soon but wtv)
handler = logging.FileHandler(filename='botserverstats.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#Bot Prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print("Bot Is Now Active And Is Monitoring Your Server")


#Restart Server
@bot.command()
async def restart(ctx):
  await ctx.reply(f"{ctx.author.mention} The Server Has Been Restarted As Per Request")
  await asyncio.create_subprocess_exec("reboot")

#ESTOP
@bot.command()
@commands.has_permissions(administrator=True)
async def ESTOP(ctx):
    await ctx.reply(
        f"{ctx.author.mention} Emergency stop triggered.\n"
        "Type `yes` to reboot or `no` to shut down.\n"
        "You have 20 seconds remaning."
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=20.0, check=check)

        if msg.content.lower() == "yes":
            await ctx.reply("Stoping...")
            await asyncio.create_subprocess_exec("reboot")

        elif msg.content.lower() == "no":
            await ctx.reply("Shutting down...")
            await asyncio.create_subprocess_exec("shutdown", "-h", "now")

        else:
            await ctx.reply("Invalid response.")

    except asyncio.TimeoutError:
        await ctx.reply("No response received.")
  
