import schedule
import time
import json

from reddit_scraper import main as scrape_posts
from post_rewriter import main as rewrite_posts
from post_to_heartbeat import post_to_heartbeat  

def run_scraping_and_posting():
    print("Starting scheduled Reddit scraping + rewriting + posting task...")

    # Step 1: Scrape new posts
    scrape_posts()

    # Step 2: Rewrite the posts
    rewrite_posts()

    # Step 3: Post to Heartbeat
    try:
        with open('rewritten_posts.json', 'r', encoding='utf-8') as f:
            rewritten_posts = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load rewritten posts: {e}")
        return

    for post in rewritten_posts:
        channel_id = post['subreddit']
        content = post['rewritten_text']
        post_to_heartbeat(channel_id, content)

    print("✅ Automated task completed successfully.\n")

# Schedule the task to run every 6 hours
schedule.every(6).hours.do(run_scraping_and_posting)

# Run immediately once (optional)
run_scraping_and_posting()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
