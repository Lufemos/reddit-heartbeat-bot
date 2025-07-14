import streamlit as st
import json
import os

from reddit_scraper import main as scrape_reddit
import post_rewriter
from post_to_heartbeat import post_to_heartbeat

# Set Streamlit layout
st.set_page_config(page_title="AI Community Builder", layout="wide")
st.title("🤖 AI-Powered Reddit to Heartbeat Automation")

st.markdown("""
Welcome to the AI Community Content Automator. This tool allows you to:
1. Scrape fresh Reddit posts by topic.
2. Rewrite them using GPT-4o for clarity and tone.
3. Post the rewritten content directly to your Heartbeat community platform.
""")

# === Step 1: Scrape Reddit ===
st.header("Step 1: Scrape Reddit Posts")

if st.button("🔍 Scrape Now"):
    with st.spinner("Collecting new posts from Reddit..."):
        scrape_reddit()
    st.success("✅ Posts scraped successfully! Check below for preview.")

# Preview scraped posts
if os.path.exists("new_posts.json"):
    with open("new_posts.json", "r", encoding="utf-8") as f:
        scraped_posts = json.load(f)
    st.subheader("📄 Preview: Scraped Posts")
    for post in scraped_posts[:5]:
        st.markdown(f"**Subreddit:** r/{post['subreddit']}")
        st.markdown(f"**Title:** {post['title']}")
        st.markdown(f"**Body:** {post.get('selftext', '')[:300]}...")
        st.markdown("---")
else:
    st.info("No scraped posts found yet.")

# === Step 2: Rewrite Posts ===
st.header("Step 2: Rewrite with GPT-4o")

if st.button("✍️ Rewrite Posts"):
    with st.spinner("Rewriting posts using GPT-4o..."):
        try:
            post_rewriter.main()
            st.success("✅ Rewriting complete. Output saved to `rewritten_posts.json`.")
        except Exception as e:
            error_msg = str(e).lower()
            if "insufficient_quota" in error_msg or "quota" in error_msg:
                st.error("❌ Your OpenAI API key has run out of quota. Please upgrade your OpenAI plan.")
                st.info("💡 You can try the paraphraser version of this app instead.")
            else:
                st.error(f"❌ An unexpected error occurred: {e}")

# Preview rewritten posts
if os.path.exists("rewritten_posts.json"):
    with open("rewritten_posts.json", "r", encoding="utf-8") as f:
        rewritten = json.load(f)
    st.subheader("✏️ Preview: Rewritten Content")
    for post in rewritten[:5]:
        st.markdown(f"**Subreddit:** r/{post['subreddit']}")
        st.text_area("Rewritten Output", value=post['rewritten_text'], height=150)
        st.markdown("---")
else:
    st.info("No rewritten posts found yet.")

# === Step 3: Post to Heartbeat ===
st.header("Step 3: Publish to Heartbeat Community")

if st.button("🚀 Post to Heartbeat"):
    if os.path.exists("rewritten_posts.json"):
        with open("rewritten_posts.json", "r", encoding="utf-8") as f:
            posts_to_publish = json.load(f)
        with st.spinner("Sending posts to Heartbeat..."):
            for post in posts_to_publish:
                post_to_heartbeat(post["subreddit"], post["rewritten_text"])
        st.success("✅ All content posted to Heartbeat!")
    else:
        st.error("⚠️ No rewritten content to post. Please rewrite posts first.")

st.markdown("---")
st.caption("Built using Streamlit + OpenAI + Reddit + Heartbeat")
