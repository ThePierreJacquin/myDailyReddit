import streamlit as st
from utils.reddit_API import get_top_posts_and_comments,display_reddit_post
import json
from stqdm import stqdm

# Set Streamlit page configuration
st.set_page_config("Slow News", layout="centered")

# Set the title for the Streamlit app
st.title("Today's News")

# Initialize session state for each subreddit
if "daily" not in st.session_state:
    subs = json.load(open("resources/subreddit_list.json"))
    daily = subs["daily"]
    monthly = subs["monthly"]
    st.session_state["daily"] = daily
    for sub in stqdm(daily, leave=False):
        st.session_state[sub] = get_top_posts_and_comments(sub)

# Create columns for each subreddit
tabs = st.tabs([f'Page {i+1} - {name}' for i,name in enumerate(daily)])

# Loop through subreddits and display their posts
for tab, sub in zip(tabs, daily):
    for post in st.session_state[sub]:
        with tab.container():
            display_reddit_post(post)
