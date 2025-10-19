#!/usr/bin/env python3
"""
Quick test to check Discord bot connection
"""

import os
import discord
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('DISCORD_BOT_TOKEN')
channel_id = int(os.getenv('DISCORD_CHANNEL_ID', 0))

print(f"Bot Token: {bot_token[:20]}..." if bot_token else "No token found")
print(f"Channel ID: {channel_id}")

# Test basic connection
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot connected as {bot.user}')
    
    # Test channel access
    channel = bot.get_channel(channel_id)
    if channel:
        print(f'✅ Found channel: {channel.name} in {channel.guild.name}')
        await channel.send("🤖 Test message from AI News Bot!")
        print("✅ Test message sent!")
    else:
        print(f'❌ Could not find channel with ID: {channel_id}')
    
    await bot.close()

try:
    bot.run(bot_token)
except Exception as e:
    print(f"❌ Error: {e}")
