import streamlit as st
import json
import os

from reddit_scraper import main as scrape_reddit
from post_rewriter import main as rewrite_posts
from post_to_heartbeat import post_to_heartbeat

st.set_page_config(page_title="AI Community Builder", layout="wide")
st.title("🤖 AI-Powered Reddit-to-Heartbeat Automation")

st.markdown("This app scrapes Reddit posts, rewrites them using GPT-4o, and posts them to your Heartbeat community.")

# === STEP 1: Scrape Reddit ===
st.header("Step 1: Scrape New Reddit Posts")

if st.button("🔍 Scrape Reddit Now"):
    with st.spinner("Scraping posts from Reddit..."):
        scrape_reddit()
    st.success("✅ Scraping completed. Posts saved to `new_posts.json`.")

# Preview scraped posts
if os.path.exists("new_posts.json"):
    with open("new_posts.json", "r", encoding="utf-8") as f:
        new_posts = json.load(f)
    st.subheader("📋 Preview of Scraped Reddit Posts")
    for post in new_posts[:5]:
        st.markdown(f"**Subreddit:** r/{post['subreddit']}")
        st.markdown(f"**Title:** {post['title']}")
        st.markdown(f"**Body:** {post.get('selftext', '')[:300]}...")
        st.markdown("---")

# === STEP 2: Rewrite Posts ===
st.header("Step 2: Rewrite Posts with GPT-4o")

if st.button("✍️ Rewrite Posts"):
    with st.spinner("Rewriting posts..."):
        rewrite_posts()
    st.success("✅ Rewriting completed. Output saved to `rewritten_posts.json`.")

# Preview rewritten posts
if os.path.exists("rewritten_posts.json"):
    with open("rewritten_posts.json", "r", encoding="utf-8") as f:
        rewritten = json.load(f)
    st.subheader("🔁 Preview of Rewritten Posts")
    for post in rewritten[:5]:
        st.markdown(f"**Subreddit:** r/{post['subreddit']}")
        st.text_area("Rewritten Text", value=post['rewritten_text'], height=150)
        st.markdown("---")

# === STEP 3: Post to Heartbeat ===
st.header("Step 3: Post to Heartbeat Community")

if st.button("🚀 Post to Heartbeat"):
    if os.path.exists("rewritten_posts.json"):
        with open("rewritten_posts.json", "r", encoding="utf-8") as f:
            posts_to_send = json.load(f)
        with st.spinner("Posting to Heartbeat..."):
            for post in posts_to_send:
                post_to_heartbeat(post["subreddit"], post["rewritten_text"])
        st.success("✅ All posts have been published to Heartbeat!")
    else:
        st.error("⚠️ No rewritten posts found. Please run Step 2 first.")

st.markdown("---")
st.caption("Built with Streamlit + OpenAI + Reddit + Heartbeat")
