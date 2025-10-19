#!/usr/bin/env python3
"""
Script to find all channels the bot can access
"""

import os
import discord
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot connected as {bot.user}')
    print(f'Bot is in {len(bot.guilds)} server(s):')
    
    for guild in bot.guilds:
        print(f'\n📋 Server: {guild.name} (ID: {guild.id})')
        print('Channels:')
        
        for channel in guild.text_channels:
            print(f'  - #{channel.name} (ID: {channel.id})')
    
    await bot.close()

try:
    bot.run(bot_token)
except Exception as e:
    print(f"❌ Error: {e}")
