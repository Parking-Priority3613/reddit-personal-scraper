import praw
import pandas as pd
import configparser
import json
import os
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
config = configparser.ConfigParser()
config.read('config.ini')

reddit = praw.Reddit(
    client_id=config['reddit']['client_id'],
    client_secret=config['reddit']['client_secret'],
    user_agent=config['reddit']['user_agent'],
    username=config['reddit']['username'],
    password=config['reddit']['password']
)

# ─────────────────────────────────────────────
# SETTINGS — edit these as needed
# ─────────────────────────────────────────────
SUBREDDITS = ['learnpython', 'datascience', 'cryptocurrency', 'webdev', 'MachineLearning']
KEYWORDS = []          # e.g. ['python', 'api'] — leave empty to fetch all
POST_LIMIT = 100       # number of posts per subreddit
SORT_BY = 'hot'        # 'hot', 'new', 'top', 'rising'
OUTPUT_FORMAT = 'csv'  # 'csv' or 'json'
OUTPUT_DIR = 'output'


def matches_keywords(text, keywords):
    """Return True if text contains any keyword (case-insensitive), or no keywords set."""
    if not keywords:
        return True
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def fetch_posts(subreddit_name):
    """Fetch posts from a subreddit."""
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    if SORT_BY == 'hot':
        feed = subreddit.hot(limit=POST_LIMIT)
    elif SORT_BY == 'new':
        feed = subreddit.new(limit=POST_LIMIT)
    elif SORT_BY == 'top':
        feed = subreddit.top(limit=POST_LIMIT)
    elif SORT_BY == 'rising':
        feed = subreddit.rising(limit=POST_LIMIT)
    else:
        feed = subreddit.hot(limit=POST_LIMIT)

    for post in feed:
        text = f"{post.title} {post.selftext}"
        if matches_keywords(text, KEYWORDS):
            posts.append({
                'subreddit': subreddit_name,
                'id': post.id,
                'title': post.title,
                'author': str(post.author),
                'score': post.score,
                'upvote_ratio': post.upvote_ratio,
                'num_comments': post.num_comments,
                'url': post.url,
                'selftext': post.selftext[:500],
                'created_utc': datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'permalink': f"https://reddit.com{post.permalink}"
            })

    print(f"  [{subreddit_name}] {len(posts)} posts fetched.")
    return posts


def save_data(data, subreddit_name):
    """Save scraped data to CSV or JSON."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{OUTPUT_DIR}/{subreddit_name}_{timestamp}"

    if OUTPUT_FORMAT == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(f"{filename}.csv", index=False, encoding='utf-8')
        print(f"  Saved: {filename}.csv")
    elif OUTPUT_FORMAT == 'json':
        with open(f"{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Saved: {filename}.json")


def main():
    print("Reddit Personal Scraper")
    print("=" * 40)
    for sub in SUBREDDITS:
        print(f"\nScraping r/{sub}...")
        posts = fetch_posts(sub)
        if posts:
            save_data(posts, sub)
    print("\nDone! All data saved to the output/ folder.")


if __name__ == '__main__':
    main()
