# 🤖 AI News Aggregator

A Python bot that collects daily AI news from multiple sources (Reddit, NewsAPI) and sends summarized updates to your Discord server using OpenAI's GPT.

## ✨ Features

- **Multi-source news collection**: Reddit AI subreddits + NewsAPI.org
- **AI-powered summarization**: Uses OpenAI GPT to create engaging summaries
- **Discord integration**: Sends formatted news to your Discord channel
- **Scheduled updates**: Daily news at 9 AM (configurable)
- **Manual trigger**: Use `!news` command for instant updates
- **Free hosting ready**: Configured for Railway, Heroku, and other platforms

## 🚀 Quick Setup

### 1. Get API Keys

**Required:**
- **NewsAPI.org**: Free tier (1,000 requests/day) - [Get key here](https://newsapi.org/register)
- **OpenAI API**: Pay-per-use - [Get key here](https://platform.openai.com/api-keys)
- **Discord Bot**: Free - [Create bot here](https://discord.com/developers/applications)

**Optional:**
- **Reddit API**: Free - [Create app here](https://www.reddit.com/prefs/apps)

### 2. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token
5. Enable "Message Content Intent" in bot settings
6. Invite bot to your server with appropriate permissions

### 3. Environment Variables

Copy `env_example.txt` to `.env` and fill in your keys:

```bash
cp env_example.txt .env
```

Required variables:
```
NEWS_API_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_api_key
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_discord_channel_id
```

### 4. Install and Run

```bash
pip install -r requirements.txt
python ai_news_aggregator.py
```

## 🌐 Free Hosting Options

### Option 1: Railway (Recommended)
1. Push code to GitHub
2. Connect GitHub repo to [Railway](https://railway.app)
3. Add environment variables in Railway dashboard
4. Deploy!

### Option 2: Heroku
1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Set environment variables: `heroku config:set KEY=value`
4. Deploy: `git push heroku main`

### Option 3: Render
1. Connect GitHub repo to [Render](https://render.com)
2. Choose "Background Worker" service type
3. Add environment variables
4. Deploy!

## 📊 News Sources

**Reddit Subreddits:**
- r/MachineLearning
- r/artificial
- r/OpenAI
- r/singularity
- r/deeplearning
- r/artificial_intelligence
- r/ChatGPT
- r/LocalLLaMA

**NewsAPI Keywords:**
- artificial intelligence
- AI
- machine learning
- deep learning
- OpenAI
- GPT
- LLM
- neural network

## 🎛️ Customization

### Change Schedule
Edit the schedule in `ai_news_aggregator.py`:
```python
schedule.every().day.at("09:00").do(lambda: asyncio.create_task(bot.send_daily_news()))
```

### Add More Sources
Add new subreddits to `self.ai_subreddits` or keywords to `self.ai_keywords`.

### Customize Summary
Modify the OpenAI prompt in the `summarize_news` method.

## 💰 Cost Breakdown

**Free/Cheap Options:**
- **NewsAPI**: Free tier (1,000 requests/day)
- **Reddit API**: Completely free
- **Discord**: Free
- **OpenAI**: ~$0.01-0.05 per day (depending on news volume)
- **Hosting**: Free on Railway/Render/Heroku

**Total estimated cost: $0.30-1.50/month**

## 🔧 Troubleshooting

### Bot not responding
- Check Discord bot token and permissions
- Ensure bot is invited to server with correct channel ID
- Verify "Message Content Intent" is enabled

### No news found
- Check NewsAPI key and rate limits
- Verify Reddit API credentials (optional)
- Check internet connection

### OpenAI errors
- Verify OpenAI API key and billing
- Check rate limits and usage quotas

## 📝 Commands

- `!news` - Manually trigger news collection
- Bot automatically sends news daily at 9 AM

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - feel free to use and modify!
