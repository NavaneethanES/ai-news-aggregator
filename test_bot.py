#!/usr/bin/env python3
"""
Test script to verify the AI News Aggregator setup
Run this to test your configuration before deploying
"""

import os
from dotenv import load_dotenv
from ai_news_aggregator import AINewsAggregator

def test_configuration():
    """Test all API configurations"""
    load_dotenv()
    
    print("🤖 AI News Aggregator - Configuration Test")
    print("=" * 50)
    
    # Test environment variables
    required_vars = {
        'NEWS_API_KEY': 'NewsAPI.org key',
        'OPENAI_API_KEY': 'OpenAI API key',
        'DISCORD_BOT_TOKEN': 'Discord bot token',
        'DISCORD_CHANNEL_ID': 'Discord channel ID'
    }
    
    optional_vars = {
        'REDDIT_CLIENT_ID': 'Reddit client ID',
        'REDDIT_CLIENT_SECRET': 'Reddit client secret'
    }
    
    print("\n📋 Checking Environment Variables:")
    all_good = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {description} - Found")
        else:
            print(f"❌ {var}: {description} - Missing")
            all_good = False
    
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {description} - Found")
        else:
            print(f"⚠️  {var}: {description} - Optional (Reddit will be skipped)")
    
    if not all_good:
        print("\n❌ Missing required environment variables!")
        print("Please check your .env file and ensure all required keys are set.")
        return False
    
    print("\n✅ All required environment variables found!")
    
    # Test API connections
    print("\n🔌 Testing API Connections:")
    
    try:
        aggregator = AINewsAggregator()
        
        # Test NewsAPI
        print("Testing NewsAPI...")
        newsapi_news = aggregator.get_newsapi_news(limit=5)
        print(f"✅ NewsAPI: Found {len(newsapi_news)} news items")
        
        # Test Reddit (if configured)
        if aggregator.reddit:
            print("Testing Reddit API...")
            reddit_news = aggregator.get_reddit_news(limit=5)
            print(f"✅ Reddit: Found {len(reddit_news)} news items")
        else:
            print("⚠️  Reddit: Skipped (not configured)")
        
        # Test OpenAI
        print("Testing OpenAI API...")
        if newsapi_news:
            summary = aggregator.summarize_news(newsapi_news[:3])
            if "Error" not in summary:
                print("✅ OpenAI: Summary generated successfully")
                print(f"Summary preview: {summary[:100]}...")
            else:
                print(f"❌ OpenAI: {summary}")
        else:
            print("⚠️  OpenAI: Skipped (no news to summarize)")
        
        print("\n🎉 Configuration test completed!")
        print("\nNext steps:")
        print("1. Run 'python ai_news_aggregator.py' to start the bot")
        print("2. Use '!news' command in Discord to test manually")
        print("3. Deploy to your preferred hosting platform")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    test_configuration()
