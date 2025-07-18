import json
import discord
from discord import app_commands
from datetime import datetime, timedelta
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import pytz
import asyncio
from dateutil.relativedelta import relativedelta # For accurate time difference

# env file se variable load karne ke liye

YOUR_GUILD_ID = 1388170909512241282 

import asyncio
import yt_dlp


import discord.ui

import random


import logging
import os

load_dotenv()
#loads the token from thr .env file
# token = os.getenv('DISCORD_BOT_TOKEN')
# If the token is not found in the environment variables, raise an error
token = os.getenv('DISCORD_BOT_TOKEN')

if not token:
    raise ValueError("DISCORD_BOT_TOKEN not found in environment variables")

# Set up logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logging.basicConfig(level=logging.INFO, handlers=[handler])

intents = discord.Intents.default()
intents.message_content = True # Required for reading message content
intents.members = True         # Required for certain member-related events
intents.voice_states = True # Required for voice state updates

bot = commands.Bot(command_prefix='.', intents=intents)

bot_data = {}

def load_bot_data():
    """Loads data from bot_data.json every time it's called."""
    try:
        with open('bot_data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty dictionary if the file is missing or broken
        return {}

@bot.event
async def on_ready():
    try:
        # The sync command tells Discord to update the command list.
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
        
    print(f"{bot.user} is online!")
@bot.event
async def on_member_join(member):
    # Send DM to the user
    await member.send(f'Welcome to the server, {member.name}!')
    print(f'{member.name} has joined the server.')
    # Send message in the system channel if it exists
    if member.guild.system_channel is not None:
        await member.guild.system_channel.send(f'Welcome to the server, {member.mention}!')

     
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('Hello'):
        await message.channel.send(f'Hello {message.author.mention}!')
    elif message.content.startswith('What time is it'):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await message.channel.send(f'Current time is: {current_time}')
    elif message.content.startswith('Seeee '):
        await message.channel.send(f'Seeee Seeeee {message.author.mention}!') 

# --- Basic Slash Command: Ping ---
@bot.tree.command(name="ping", description="Checks the bot's latency (response time).")
async def ping(interaction: discord.Interaction):
    latency_ms = round(bot.latency * 1000) # bot.latency is in seconds, convert to milliseconds
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"My response time is **{latency_ms}ms**.",
        color=discord.Color.from_rgb(0, 200, 255) # A nice blue color
    )
    await interaction.response.send_message(embed=embed)

    #  --- Basic Slash Command: Hello ---
@bot.tree.command(name="hello", description="Says hello to the user.")
async def hello(interaction: discord.Interaction):
    embed = discord.Embed(
        title="👋 Hello!",
        description=f"Hello **{interaction.user.mention}!** How can I assist you today?",
        color=discord.Color.from_rgb(0, 200, 255) # A nice blue color
    )
    await interaction.response.send_message(embed=embed)

# --- Anniversary & Personalized Commands ---

@bot.tree.command(name="memory", description="Shares a random sweet memory from our journey.")
async def memory(interaction: discord.Interaction):
    bot_data = load_bot_data()
    memories = bot_data.get("sweet_memories", ["No sweet memories defined yet! Please add some to bot_data.json."])
    if memories:
        chosen_memory = random.choice(memories)
        embed = discord.Embed(
            title="✨ A Sweet Memory ✨",
            description=f"💖 {chosen_memory}",
            color=discord.Color.from_rgb(255, 192, 203) # Light Pink
        )
        # Optional: Replace with a tiny heart or photo URL for the thumbnail
        # embed.set_image(url="YOUR_IMAGE_URL_HERE") 
        # embed.set_thumbnail(url="https://i.imgur.com/your_memory_thumbnail_url.png")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No sweet memories found. Please add some to bot_data.json!")

@bot.tree.command(name="firsts", description="Recalls a special 'first' moment from our relationship.")
# Define the 'moment' argument and its choices
@app_commands.describe(moment="Choose which 'first' moment to recall.")
@app_commands.choices(moment=[
    # Iterate through your bot_data.json to create these choices automatically
    # NOTE: These must be hardcoded here for Discord's API to register them.
    # You need to manually update this section if you add new 'firsts' to bot_data.json
    app_commands.Choice(name="First Met", value="first_met"),
    app_commands.Choice(name="First Date", value="first_date"),
    app_commands.Choice(name="First I Love You", value="first_i_love_you"),
    app_commands.Choice(name="First Confession Dory", value="first_confession_dory"),
    app_commands.Choice(name="First Confession Sid", value="first_confession_sid")
    # Add more app_commands.Choice lines here if you add more "firsts" to bot_data.json
])
async def firsts(interaction: discord.Interaction, moment: str):
    bot_data = load_bot_data()
    first_moments = bot_data.get("first_moments", {})
    
    # The 'moment' variable will now directly contain the chosen 'value' (e.g., "first_met")
    chosen_moment_key = moment 

    if chosen_moment_key in first_moments:
        description = first_moments[chosen_moment_key]
        embed = discord.Embed(
            title=f"❤️ Our First: {chosen_moment_key.replace('_', ' ').title()} ❤️", # Title case for display
            description=description,
            color=discord.Color.from_rgb(255, 105, 180) # Hot Pink
        )
        await interaction.response.send_message(embed=embed)
    else:
        # This else block should ideally not be hit if choices are properly defined
        embed = discord.Embed(
            title="🤔 Error",
            description=f"An unexpected error occurred for moment: {chosen_moment_key}.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="oursong", description="Suggests a random song that's meaningful to us.")
async def oursong(interaction: discord.Interaction):
    bot_data = load_bot_data()
    songs = bot_data.get("our_songs", [])
    if songs:
        chosen_song = random.choice(songs)
        embed = discord.Embed(
            title="🎶 Our Special Song 🎶",
            description=f"**{chosen_song.get('title', 'Unknown Title')}** by {chosen_song.get('artist', 'Unknown Artist')}",
            color=discord.Color.from_rgb(147, 112, 219) # Medium Purple
        )
        if chosen_song.get('link'):
            embed.add_field(name="Listen here:", value=f"[Link]({chosen_song['link']})", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No special songs defined in bot_data.json yet!")        



@bot.tree.command(name="futureadventure", description="Suggests a fun idea for our next adventure!")
async def futureadventure(interaction: discord.Interaction):
    bot_data = load_bot_data() 
    adventures = bot_data.get("future_adventures", ["No future adventures defined yet! Please add some to bot_data.json."])
    if adventures:
        chosen_adventure = random.choice(adventures)
        embed = discord.Embed(
            title="🗺️ Our Next Adventure! 🚀",
            description=f"How about: **{chosen_adventure}**",
            color=discord.Color.from_rgb(255, 165, 0) # Orange
        )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No future adventures found. Please add some to bot_data.json!")


@bot.tree.command(name="iloveyou", description="A special message just for you.")
async def iloveyou(interaction: discord.Interaction):
    bot_data = load_bot_data()
    compliments = bot_data.get("compliments", ["You're simply amazing!", "No compliments defined yet! Please add some to bot_data.json."])
    if compliments:
        chosen_compliment = random.choice(compliments)
        embed = discord.Embed(
            title="💖 Just For You, Dory 💖",
            description=f" **{chosen_compliment}**",
            color=discord.Color.from_rgb(0, 255, 255) # Cyan
                            )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No compliments found. Please add some to bot_data.json!")


@bot.tree.command(name="mypoems", description="Shares a beautiful poem from my heart.")
async def mypoems(interaction: discord.Interaction):
    bot_data = load_bot_data()
    poems = bot_data.get("my_poems", ["No poems defined yet! Please add some to bot_data.json."])
    if poems:
        chosen_poem = random.choice(poems)
        embed = discord.Embed(
            title="📜 A Poem For You 📜",
            description=f"*{chosen_poem}*", # Italicize the poem
            color=discord.Color.from_rgb(153, 50, 204) # Rebecca Purple
        )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No poems found. Please add some to bot_data.json!")

# --- Anniversary Command ---
@bot.tree.command(name="anniversary", description="Shows the countdown to our anniversary!")
async def anniversary(interaction: discord.Interaction):
    bot_data = load_bot_data()
    # --- FIX 1: Load data fresh from the file every time ---
    try:
        with open('bot_data.json', 'r') as f:
            bot_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        await interaction.response.send_message("Error: Could not read or parse bot_data.json.", ephemeral=True)
        return

    anniversary_str = bot_data.get("anniversary_date")
    if not anniversary_str:
        await interaction.response.send_message("Anniversary date not set in bot_data.json! Please configure it.", ephemeral=True)
        return

    try:
        # --- FIX 2: Make dates timezone-aware ---
        IST = pytz.timezone('Asia/Kolkata')
        naive_anniversary_dt = datetime.strptime(anniversary_str, "%Y-%m-%d %H:%M:%S")
        anniversary_dt = IST.localize(naive_anniversary_dt)
        now = datetime.now(IST)

    except (ValueError, pytz.UnknownTimeZoneError):
        await interaction.response.send_message("Error: Invalid date format in bot_data.json. Use `YYYY-MM-DD HH:MM:SS`.", ephemeral=True)
        return

    if now < anniversary_dt:
        # --- FIX 3: Use accurate time calculation and clean up logic ---
        time_left = relativedelta(anniversary_dt, now)

        countdown_parts = []
        if time_left.years > 0:
            countdown_parts.append(f"**{time_left.years}** {'year' if time_left.years == 1 else 'years'}")
        if time_left.months > 0:
            countdown_parts.append(f"**{time_left.months}** {'month' if time_left.months == 1 else 'months'}")
        if time_left.days > 0:
            countdown_parts.append(f"**{time_left.days}** {'day' if time_left.days == 1 else 'days'}")
        
        countdown_parts.append(f"**{time_left.hours}** {'hour' if time_left.hours == 1 else 'hours'}")
        countdown_parts.append(f"**{time_left.minutes}** {'minute' if time_left.minutes == 1 else 'minutes'}")
        countdown_parts.append(f"**{time_left.seconds}** {'second' if time_left.seconds == 1 else 'seconds'}")

        countdown_str = ", ".join(countdown_parts)
        
        embed = discord.Embed(
            title="⏳ Anniversary Countdown! ⏳",
            description=f"Our special day is in:\n{countdown_str}",
            color=discord.Color.from_rgb(173, 216, 230) # Light Blue
        )
        embed.set_footer(text=f"Mark your calendars for {anniversary_dt.strftime('%B %d, %Y at %I:%M %p %Z')}")

    else:
        embed = discord.Embed(
            title="🎉 Happy Anniversary! 🎉",
            description="💖 We're celebrating our special day right now!",
            color=discord.Color.from_rgb(255, 215, 0) # Gold
        )
        
    await interaction.response.send_message(embed=embed)
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
