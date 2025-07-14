import json
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY is not set.")
client = OpenAI(api_key=OPENAI_API_KEY)

# File paths
POSTS_FILE = "new_posts.json"
REWRITTEN_FILE = "rewritten_posts.json"

def rewrite_post(title, body):
    prompt = (
        "Rewrite the following Reddit post title and body. Make it clear, engaging, and unique, "
        "while keeping the original meaning.\n\n"
        f"Title: {title.strip()}\n\n"
        f"Body: {body.strip()}\n\n"
        "Rewritten Title and Body:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You rewrite Reddit posts to be clearer and more engaging."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[ERROR] GPT failed to rewrite post: {e}")
        return None

def main():
    try:
        with open(POSTS_FILE, "r", encoding="utf-8") as f:
            posts = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read {POSTS_FILE}: {e}")
        return

    rewritten_posts = []

    for idx, post in enumerate(posts):
        print(f"Rewriting post {idx + 1}/{len(posts)} from r/{post.get('subreddit', 'unknown')}...")

        rewritten = rewrite_post(post.get("title", ""), post.get("selftext", ""))

        if rewritten:
            rewritten_posts.append({
                "original_id": post["id"],
                "subreddit": post["subreddit"],
                "rewritten_text": rewritten
            })
        else:
            print(f"[SKIPPED] Post ID {post['id']} could not be rewritten.")

        time.sleep(1.2)

    try:
        with open(REWRITTEN_FILE, "w", encoding="utf-8") as f:
            json.dump(rewritten_posts, f, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Rewritten posts saved to {REWRITTEN_FILE}")
    except Exception as e:
        print(f"[ERROR] Failed to write to {REWRITTEN_FILE}: {e}")

if __name__ == "__main__":
    main()
