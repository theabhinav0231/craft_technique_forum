import streamlit as st
from datetime import datetime
import uuid # To generate unique IDs for topics and posts

# --- Page Configuration ---
st.set_page_config(
    page_title="Craft Knowledge Forum",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Structure (Using Session State for Demo) ---
# In a real app, replace this with database interactions.

# Initialize session state variables if they don't exist
if 'topics' not in st.session_state:
    # Example topics to start with
    st.session_state.topics = {
        "topic_1": {
            "id": "topic_1",
            "title": "Best way to sharpen chisels for detailed carving?",
            "author": "Woodworker_Pro",
            "timestamp": datetime(2025, 4, 10, 10, 30, 0),
            "posts": [
                {
                    "id": "post_1a",
                    "author": "Woodworker_Pro",
                    "content": "I'm working with intricate details on hardwood and find my chisels dull quickly. What sharpening stones or techniques do you recommend for maintaining a razor edge without removing too much metal?",
                    "timestamp": datetime(2025, 4, 10, 10, 30, 0)
                },
                {
                    "id": "post_1b",
                    "author": "SharpEdgeMaster",
                    "content": "I swear by Japanese water stones, starting with 1000 grit and progressing to 6000 or even 8000 grit. Use a honing guide to maintain a consistent angle. Finish with stropping on leather with honing compound. Takes time but the edge is incredible!",
                    "timestamp": datetime(2025, 4, 11, 9, 15, 0)
                },
                 {
                    "id": "post_1c",
                    "author": "BeginnerBuilder",
                    "content": "Thanks @SharpEdgeMaster! Do you need to flatten the water stones often? How do you do that?",
                    "timestamp": datetime(2025, 4, 11, 11, 20, 0)
                }
            ]
        },
        "topic_2": {
            "id": "topic_2",
            "title": "Troubleshooting inconsistent glaze results in pottery",
            "author": "ClayCrafter",
            "timestamp": datetime(2025, 4, 11, 14, 0, 0),
            "posts": [
                {
                    "id": "post_2a",
                    "author": "ClayCrafter",
                    "content": "My last batch of bowls came out with very different glaze colors and textures, even though I used the same glaze recipe and firing schedule. Any ideas what could cause this variation? Maybe thickness application?",
                    "timestamp": datetime(2025, 4, 11, 14, 0, 0)
                }
            ]
        }
    }

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'list_topics' # 'list_topics' or 'view_thread' or 'create_topic'

if 'selected_topic_id' not in st.session_state:
    st.session_state.selected_topic_id = None

if 'username' not in st.session_state:
    st.session_state.username = ""


# --- Utility Functions ---
def format_timestamp(ts):
    """Formats datetime object into a readable string."""
    # Using current date from context: Saturday, April 12, 2025
    # Example: 2025-04-11 09:15 AM
    return ts.strftime("%Y-%m-%d %I:%M %p")

# --- UI Components ---

# --- Sidebar ---
with st.sidebar:
    st.title("🛠️ Craft Forum")
    st.divider()

    # Simple User Identification
    st.subheader("Your Details")
    username_input = st.text_input("Enter your username", value=st.session_state.username, key="username_input_key")
    if username_input:
        st.session_state.username = username_input
    # Removed redundant else block causing potential issues on rerun

    st.divider()
    st.subheader("Actions")
    if st.button("💬 View All Topics", use_container_width=True):
        st.session_state.current_view = 'list_topics'
        st.session_state.selected_topic_id = None
        st.rerun() # Rerun to update the main view

    # Ensure username exists before enabling create topic button
    create_topic_disabled = not bool(st.session_state.username)
    create_topic_help = "Enter a username to create topics." if create_topic_disabled else None

    if st.button("➕ Create New Topic", use_container_width=True, type="primary", disabled=create_topic_disabled, help=create_topic_help):
        st.session_state.current_view = 'create_topic'
        st.session_state.selected_topic_id = None
        st.rerun()


    st.divider()
    st.caption("Part of the Cross-Generation Knowledge Transfer Platform")


# --- Main Content Area ---

# --- View: List All Topics ---
if st.session_state.current_view == 'list_topics':
    st.title("Forum Topics")
    st.markdown("Browse questions and discussions on various techniques.")
    st.divider()

    if not st.session_state.topics:
        st.info("No topics yet. Be the first to create one!")
    else:
        # Sort topics by timestamp, newest first
        sorted_topic_ids = sorted(st.session_state.topics.keys(), key=lambda tid: st.session_state.topics[tid]['timestamp'], reverse=True)

        for topic_id in sorted_topic_ids:
            topic = st.session_state.topics[topic_id]
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.subheader(topic['title'])
                    st.caption(f"Started by: **{topic['author']}** on {format_timestamp(topic['timestamp'])}")
                with col2:
                     # Calculate replies (total posts - 1 for the OP)
                     reply_count = max(0, len(topic['posts']) - 1)
                     st.metric(label="Replies", value=reply_count)
                with col3:
                     # Button to view the full thread
                     if st.button("View Thread", key=f"view_{topic_id}", use_container_width=True):
                        st.session_state.current_view = 'view_thread'
                        st.session_state.selected_topic_id = topic_id
                        st.rerun()


# --- View: Display a Single Thread ---
elif st.session_state.current_view == 'view_thread' and st.session_state.selected_topic_id:
    topic_id = st.session_state.selected_topic_id
    if topic_id not in st.session_state.topics:
        st.error("Topic not found!")
        st.session_state.current_view = 'list_topics' # Go back to list if topic deleted/invalid
        st.session_state.selected_topic_id = None
        st.rerun()
    else:
        topic = st.session_state.topics[topic_id]

        st.title(f"🧵 {topic['title']}")

        # --- Display Original Post (OP) ---
        if topic['posts']: # Check if there are any posts
            op_post = topic['posts'][0]
            col1, col2 = st.columns([3, 1]) # Author on left, Timestamp on right
            with col1:
                st.markdown(f"**{op_post['author']}** (OP)")
            with col2:
                # Use markdown with inline HTML for right alignment
                st.markdown(f"<p style='text-align: right; color: grey; font-size: smaller;'>{format_timestamp(op_post['timestamp'])}</p>", unsafe_allow_html=True)

            st.markdown(op_post['content']) # Display OP content directly
            st.divider() # Separator after OP content

        # --- Display Replies ---
        if len(topic['posts']) > 1: # Check if there are replies
            st.subheader(f"Replies ({len(topic['posts']) - 1})")
            # Loop through replies (all posts *except* the first one)
            for i, reply in enumerate(topic['posts'][1:]):
                # Add a divider *before* each reply container (but not before the very first reply shown)
                # The first divider is already added after the OP post.
                if i > 0: # Add divider before the 2nd, 3rd, etc. reply
                     st.divider()

                with st.container(): # Using container without border for replies now, divider provides separation
                    col1_reply, col2_reply = st.columns([3, 1]) # Author left, Timestamp right
                    with col1_reply:
                        st.markdown(f"**{reply['author']}**")
                    with col2_reply:
                        st.markdown(f"<p style='text-align: right; color: grey; font-size: smaller;'>{format_timestamp(reply['timestamp'])}</p>", unsafe_allow_html=True)

                    st.markdown(reply['content']) # Display reply content

            st.divider() # Add a final divider after the last reply, before the reply box

        # --- Reply Form ---
        st.subheader("💬 Add Your Reply")
        if st.session_state.username:
            with st.form("reply_form", clear_on_submit=True):
                reply_content = st.text_area("Your message:", height=150, placeholder="Share your insights or ask for clarification...")
                submitted = st.form_submit_button("Post Reply")

                if submitted:
                    if not reply_content.strip():
                        st.warning("Reply cannot be empty.")
                    else:
                        new_post_id = f"post_{uuid.uuid4().hex[:8]}" # Generate unique ID
                        new_post = {
                            "id": new_post_id,
                            "author": st.session_state.username,
                            "content": reply_content,
                            "timestamp": datetime.now()
                        }
                        st.session_state.topics[topic_id]['posts'].append(new_post)
                        st.success("Reply posted successfully!")
                        st.rerun() # Rerun to show the new post immediately
        else:
            st.warning("Please enter your username in the sidebar to reply.")

# --- View: Create New Topic ---
elif st.session_state.current_view == 'create_topic':
    st.title("➕ Start a New Discussion")
    st.markdown("Ask a question or share a technique.")
    st.divider()

    if not st.session_state.username:
         st.error("Error: Username is required to create a topic. Please enter it in the sidebar.")
         # Optionally redirect back or disable form
    else:
        with st.form("new_topic_form", clear_on_submit=True):
            topic_title = st.text_input("Topic Title / Question:", placeholder="e.g., How to achieve a perfect dovetail joint?")
            topic_content = st.text_area("Your first post (provide details):", height=200, placeholder="Describe the technique, problem, or question in detail...")

            submitted = st.form_submit_button("Create Topic")

            if submitted:
                if not topic_title.strip():
                    st.warning("Topic title cannot be empty.")
                elif not topic_content.strip():
                    st.warning("The first post cannot be empty.")
                else:
                    new_topic_id = f"topic_{uuid.uuid4().hex[:8]}" # Generate unique ID
                    first_post_id = f"post_{uuid.uuid4().hex[:8]}"
                    timestamp = datetime.now()

                    new_topic = {
                        "id": new_topic_id,
                        "title": topic_title,
                        "author": st.session_state.username,
                        "timestamp": timestamp,
                        "posts": [
                            {
                                "id": first_post_id,
                                "author": st.session_state.username,
                                "content": topic_content,
                                "timestamp": timestamp
                            }
                        ]
                    }
                    st.session_state.topics[new_topic_id] = new_topic
                    st.success("Topic created successfully!")

                    # Switch view to the newly created topic
                    st.session_state.current_view = 'view_thread'
                    st.session_state.selected_topic_id = new_topic_id
                    st.rerun() # Rerun to show the new topic view