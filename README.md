# Reddit Personal Scraper

A lightweight, read-only Reddit scraper built with Python and PRAW (Python Reddit API Wrapper) for personal research and data analysis.

## Features

- Fetch posts and comments from any public subreddit
- Keyword-based filtering
- Export data to CSV or JSON
- Fully respects Reddit API rate limits
- Read-only: no posting, voting, or write operations
- Local storage only — no data sharing or redistribution

## Project Structure

```
reddit-personal-scraper/
├── scraper.py          # Main scraper script
├── config.example.ini  # Example configuration file
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Parking-Priority3613/reddit-personal-scraper.git
cd reddit-personal-scraper
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure credentials
- Copy `config.example.ini` to `config.ini`
- Register a Reddit app at https://www.reddit.com/prefs/apps (select **script**)
- Fill in your `client_id`, `client_secret`, and `username`

```bash
cp config.example.ini config.ini
```

### 4. Run the scraper
```bash
python scraper.py
```

## Usage

Edit the `scraper.py` file to set:
- Target subreddits
- Keywords to filter
- Number of posts to fetch
- Output format (CSV or JSON)

## Legal & Ethics

- This tool is for **personal use only**
- Complies with [Reddit's API Terms of Service](https://www.redditinc.com/policies/data-api-terms)
- Respects rate limits (max 60 requests/min)
- No data redistribution or commercial use

## Requirements

- Python 3.8+
- PRAW 7.x
- pandas
- configparser

## License

MIT License — for personal use only.
