import praw
import pandas as pd
import json
import os

# --- Reddit API credentials ---
CLIENT_ID = 'IsOglfmDeSjw1JAQhLpJmg'       # Replace with your client_id
CLIENT_SECRET = '-fht7TaDTcNu5zBy-p0MVTuO1nenAQ'  # Replace with your client_secret
USER_AGENT = 'HeartbeatScraperBot/1.0'    # Descriptive user agent

# --- Files ---
EXCEL_FILE = 'AI Community SOP.xlsx'       # Your Excel file in the same folder
POSTS_ID_FILE = 'scraped_post_ids.json'   # File to track scraped post IDs
NEW_POSTS_FILE = 'new_posts.json'          # File to save newly scraped posts

def parse_channel_mappings(excel_file_path):
    df = pd.read_excel(excel_file_path, sheet_name='Channelssubreddit')
    mappings = {}
    for _, row in df.iterrows():
        channel = row['Heartbeat Channel Name']
        subreddits = []
        for col in ['Srape from Subreddit 1', 'Srape from Subreddit 2', 'Srape from Subreddit 3']:
            sub = row.get(col)
            if pd.notna(sub):
                subreddits.append(sub.strip())
        if subreddits:
            mappings[channel] = subreddits
    return mappings

def get_reddit_instance():
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        check_for_async=False
    )

def load_scraped_ids():
    if os.path.exists(POSTS_ID_FILE):
        with open(POSTS_ID_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_scraped_ids(ids):
    with open(POSTS_ID_FILE, 'w') as f:
        json.dump(list(ids), f)

def fetch_new_posts(reddit, subreddit_name, scraped_ids, limit=10):
    new_posts = []
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=limit):
            if submission.id not in scraped_ids:
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'url': submission.url,
                    'created_utc': submission.created_utc,
                    'author': str(submission.author),
                    'subreddit': subreddit_name
                }
                new_posts.append(post_data)
    except Exception as e:
        print(f"Warning: Could not fetch posts from r/{subreddit_name}: {e}")
    return new_posts

def main():
    print("Parsing subreddit-channel mappings from Excel...")
    channel_map = parse_channel_mappings(EXCEL_FILE)
    print(f"Loaded {len(channel_map)} Heartbeat channels.")

    reddit = get_reddit_instance()
    scraped_ids = load_scraped_ids()
    print(f"Loaded {len(scraped_ids)} previously scraped post IDs.\n")

    all_new_posts = []
    for channel, subreddits in channel_map.items():
        print(f"Scraping subreddits for Heartbeat channel: {channel}")
        for sub in subreddits:
            new_posts = fetch_new_posts(reddit, sub, scraped_ids)
            print(f"  Found {len(new_posts)} new posts in r/{sub}")
            all_new_posts.extend(new_posts)

    if not all_new_posts:
        print("\nNo new posts found. Exiting.")
        return

    print(f"\nTotal new posts found: {len(all_new_posts)}")
    for post in all_new_posts:
        print(f"[{post['subreddit']}] {post['title'][:80]}...")

    # Save newly scraped posts to JSON for rewriting
    with open(NEW_POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_new_posts, f, ensure_ascii=False, indent=2)
    print(f"\nSaved new posts to {NEW_POSTS_FILE}")

    # Update and save scraped IDs
    for post in all_new_posts:
        scraped_ids.add(post['id'])
    save_scraped_ids(scraped_ids)
    print(f"Updated scraped post IDs. Total tracked: {len(scraped_ids)}")

if __name__ == "__main__":
    main()
