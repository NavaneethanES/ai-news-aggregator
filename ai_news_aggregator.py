import os
import requests
import praw
import openai
import discord
from discord.ext import commands
import schedule
import time
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import List, Dict
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AINewsAggregator:
    def __init__(self):
        # Initialize APIs
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Reddit setup (optional)
        reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        reddit_user_agent = os.getenv('REDDIT_USER_AGENT', 'AI_News_Bot/1.0')
        
        if reddit_client_id and reddit_client_secret and reddit_client_id != 'your_reddit_client_id':
            self.reddit = praw.Reddit(
                client_id=reddit_client_id,
                client_secret=reddit_client_secret,
                user_agent=reddit_user_agent
            )
        else:
            self.reddit = None
            logger.warning("Reddit API not configured - will skip Reddit news")
        
        # OpenAI setup
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        else:
            logger.error("OpenAI API key not found!")
        
        # AI-related subreddits
        self.ai_subreddits = [
            'MachineLearning',
            'artificial',
            'OpenAI',
            'singularity',
            'deeplearning',
            'artificial_intelligence',
            'ChatGPT',
            'LocalLLaMA'
        ]
        
        # AI keywords for news filtering
        self.ai_keywords = os.getenv('AI_KEYWORDS', 
            'artificial intelligence,AI,machine learning,deep learning,OpenAI,GPT,LLM,neural network').split(',')

    def get_reddit_news(self, limit: int = 10) -> List[Dict]:
        """Fetch trending AI news from Reddit"""
        if not self.reddit:
            return []
        
        news_items = []
        
        for subreddit_name in self.ai_subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get hot posts from the last 24 hours
                for submission in subreddit.hot(limit=limit):
                    # Filter posts from last 24 hours
                    post_time = datetime.fromtimestamp(submission.created_utc)
                    if post_time > datetime.now() - timedelta(days=1):
                        news_items.append({
                            'title': submission.title,
                            'url': submission.url,
                            'score': submission.score,
                            'subreddit': subreddit_name,
                            'source': 'Reddit',
                            'created_at': post_time.isoformat(),
                            'comments_count': submission.num_comments
                        })
            except Exception as e:
                logger.error(f"Error fetching from r/{subreddit_name}: {e}")
        
        # Sort by score and return top items
        news_items.sort(key=lambda x: x['score'], reverse=True)
        return news_items[:20]

    def get_newsapi_news(self, limit: int = 20) -> List[Dict]:
        """Fetch AI news from NewsAPI"""
        if not self.news_api_key:
            logger.warning("NewsAPI key not found - skipping NewsAPI")
            return []
        
        news_items = []
        
        # Search for AI-related news
        for keyword in self.ai_keywords[:3]:  # Limit to avoid rate limits
            try:
                url = 'https://newsapi.org/v2/everything'
                params = {
                    'q': keyword,
                    'apiKey': self.news_api_key,
                    'sortBy': 'publishedAt',
                    'from': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                    'pageSize': 10,
                    'language': 'en'
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                for article in data.get('articles', []):
                    if article.get('title') and article.get('url'):
                        news_items.append({
                            'title': article['title'],
                            'url': article['url'],
                            'description': article.get('description', ''),
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'published_at': article.get('publishedAt', ''),
                            'keyword': keyword
                        })
                        
            except Exception as e:
                logger.error(f"Error fetching NewsAPI for keyword '{keyword}': {e}")
        
        # Remove duplicates and sort by published date
        seen_titles = set()
        unique_news = []
        for item in news_items:
            if item['title'] not in seen_titles:
                seen_titles.add(item['title'])
                unique_news.append(item)
        
        return unique_news[:limit]

    def summarize_news(self, news_items: List[Dict]) -> str:
        """Use OpenAI to create a summary of the news"""
        if not self.openai_api_key or not news_items:
            return "No news to summarize or OpenAI API key not configured."
        
        # Prepare news text for summarization
        news_text = "AI News Summary for " + datetime.now().strftime('%Y-%m-%d') + ":\n\n"
        
        for i, item in enumerate(news_items[:15], 1):  # Limit to top 15 items
            source_info = f"[{item.get('source', 'Unknown')}]"
            if 'subreddit' in item:
                source_info = f"[Reddit r/{item['subreddit']}]"
            
            news_text += f"{i}. {item['title']} {source_info}\n"
            if item.get('description'):
                news_text += f"   {item['description'][:200]}...\n"
            news_text += "\n"
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an AI news curator. Create a concise, engaging summary of the day's most important AI news and announcements. Focus on the most significant developments, breakthroughs, and announcements. Keep it under 1000 words and make it easy to read."
                    },
                    {
                        "role": "user", 
                        "content": f"Please summarize these AI news items:\n\n{news_text}"
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error creating summary: {e}")
            return f"Error creating summary: {str(e)}"

    def collect_daily_news(self) -> str:
        """Main method to collect and summarize daily AI news"""
        logger.info("Starting daily AI news collection...")
        
        # Collect news from all sources
        reddit_news = self.get_reddit_news()
        newsapi_news = self.get_newsapi_news()
        
        # Combine and deduplicate
        all_news = reddit_news + newsapi_news
        
        logger.info(f"Collected {len(all_news)} news items")
        
        if not all_news:
            return "No AI news found for today. 🤖"
        
        # Create summary
        summary = self.summarize_news(all_news)
        
        # Add source links
        summary += "\n\n📰 **Source Links:**\n"
        for i, item in enumerate(all_news[:10], 1):
            summary += f"{i}. [{item['title'][:60]}...]({item['url']})\n"
        
        return summary

# Discord Bot
class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.messages = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.news_aggregator = AINewsAggregator()
        self.channel_id = int(os.getenv('DISCORD_CHANNEL_ID', 0))

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Channel ID: {self.channel_id}')
        
        # Test channel access
        channel = self.get_channel(self.channel_id)
        if channel:
            logger.info(f'Found channel: {channel.name} in {channel.guild.name}')
        else:
            logger.error(f'Could not find channel with ID: {self.channel_id}')
            logger.info('Make sure the bot has access to the channel and the channel ID is correct')

    async def send_daily_news(self):
        """Send daily AI news to Discord channel"""
        try:
            channel = self.get_channel(self.channel_id)
            if not channel:
                logger.error(f"Channel with ID {self.channel_id} not found")
                return
            
            news_summary = self.news_aggregator.collect_daily_news()
            
            # Create embed for better formatting
            embed = discord.Embed(
                title="🤖 Daily AI News Digest",
                description=news_summary,
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.set_footer(text="AI News Aggregator Bot")
            
            await channel.send(embed=embed)
            logger.info("Daily news sent to Discord successfully!")
            
        except Exception as e:
            logger.error(f"Error sending news to Discord: {e}")

    async def on_message(self, message):
        """Handle messages"""
        if message.author == self.user:
            return
        
        if message.content.startswith('!news'):
            await message.channel.send("🔄 Fetching latest AI news...")
            try:
                news_summary = self.news_aggregator.collect_daily_news()
                
                # Create embed for better formatting
                embed = discord.Embed(
                    title="🤖 Daily AI News Digest",
                    description=news_summary,
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="AI News Aggregator Bot")
                
                await message.channel.send(embed=embed)
                logger.info("Manual news sent to Discord successfully!")
                
            except Exception as e:
                logger.error(f"Error sending manual news: {e}")
                await message.channel.send(f"❌ Error fetching news: {str(e)}")
        
        elif message.content.startswith('!test'):
            await message.channel.send("✅ Bot is working! Use `!news` to get AI news.")
        
        # Process commands
        await self.process_commands(message)

def main():
    """Main function to run the bot"""
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    if not bot_token:
        logger.error("Discord bot token not found!")
        return
    
    bot = DiscordBot()
    
    # Run the bot
    bot.run(bot_token)

if __name__ == "__main__":
    import asyncio
    main()
