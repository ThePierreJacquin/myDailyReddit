import praw
from datetime import datetime, timedelta
import streamlit as st

def get_top_posts_and_comments(subreddit_name):
    """
    Fetch top posts and comments from a given subreddit.

    Args:
        subreddit_name (str): The name of the subreddit to fetch posts from.

    Returns:
        list: A list of dictionaries containing post details and comments.
    """
    # Initialize Reddit API client
    reddit = praw.Reddit(
        client_id='hdj53lFYHh-iXf7OXGUlcA',
        client_secret='5_NFVGyTYjRhrrmpBlst29lfUZWuGA',
        user_agent='pklopklo'
    )

    # Define the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Fetch the top 10 posts from yesterday
    top_posts = subreddit.top(time_filter='day', limit=10)

    # Prepare the output data structure
    results = []

    for post in top_posts:
        post_data = {
            'title': post.title,
            'url': post.url,
            'comments': []
        }

        # Try to extract the text of the post if available
        try:
            post_data["text"] = post.selftext
        except AttributeError:
            post_data["text"] = ""

        # Check if the post contains a video
        if post.media and "reddit_video" in post.media:
            post_data["video"] = post.media["reddit_video"]["fallback_url"]

        # Fetch the top 3 comments for each post
        post.comment_sort = 'top'
        post.comments.replace_more(limit=0)
        top_comments = post.comments[:5]

        for comment in top_comments:
            post_data['comments'].append(comment.body)

        results.append(post_data)

    return results


def display_reddit_post(post):
    """
    Fetch top posts and comments from a given subreddit.

    Args:
        post (dict): A dictionnary containing post details and comments.

    Returns:
        None.
    """

    st.title(post["title"])

    # Display the appropriate media content (image, video, or text)
    if post["url"].endswith(".jpeg"):
        st.image(post["url"])
    elif "video" in post:
        st.video(post["video"])
    else:
        st.write(post["text"])

    # Display comments in an expander
    with st.expander("Comments"):
        for comment in post["comments"]:
            with st.chat_message("user",):    
                st.info(comment)
        

if __name__ == "__main__":
    get_top_posts_and_comments("ufc")
