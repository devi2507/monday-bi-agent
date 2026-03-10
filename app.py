import streamlit as st
from monday_api import fetch_board
from agent import ask_agent
from data_cleaning import clean_dataframe

# Board IDs
WORK_BOARD_ID = 5027109035
DEALS_BOARD_ID = 5027109035

st.set_page_config(
    page_title="Monday BI Agent",
    page_icon="",
    layout="wide"
)

st.title("Monday Business Intelligence Agent")
st.markdown("Ask questions about deals, pipeline, and work orders.")


# ------------------------------
# CHAT SESSION MANAGEMENT
# ------------------------------

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "suggested_question" not in st.session_state:
    st.session_state.suggested_question = None


# ------------------------------
# Sidebar
# ------------------------------

with st.sidebar:

    st.header("Chats")

    # New Chat Button
    if st.button("➕ New Chat"):

        new_chat = f"Chat {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[new_chat] = []
        st.session_state.current_chat = new_chat


    st.markdown("---")

    st.subheader("Saved Chats")

    for chat in st.session_state.chat_sessions.keys():

        if st.button(chat, use_container_width=True):
            st.session_state.current_chat = chat


    st.markdown("---")

    st.header("Agent Controls")

    if st.button("Clear Current Chat"):
        st.session_state.chat_sessions[st.session_state.current_chat] = []


    st.markdown("---")

    st.subheader("Data Sources")

    st.write("• Deals Board")
    st.write("• Work Orders Board")


    st.markdown("---")

    st.subheader("Suggested Questions")

    suggestions = [
        "Summarize operational performance",
        "How many projects are completed?",
        "Which type of work is most common?",
        "Are there projects not started yet?"
    ]

    for q in suggestions:
        if st.button(q):
            st.session_state.suggested_question = q


# ------------------------------
# Get Current Chat Messages
# ------------------------------

messages = st.session_state.chat_sessions[st.session_state.current_chat]


# ------------------------------
# Display Chat History
# ------------------------------

for message in messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ------------------------------
# User Input
# ------------------------------

query = st.chat_input("Ask a business question")

if st.session_state.suggested_question:
    query = st.session_state.suggested_question
    st.session_state.suggested_question = None


# ------------------------------
# Handle User Query
# ------------------------------

if query:

    # Show user message
    messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)


    # Fetch and process data
    with st.spinner("Analyzing business data..."):

        try:

            deals_df = fetch_board(DEALS_BOARD_ID)
            work_df = fetch_board(WORK_BOARD_ID)

        except Exception as e:

            st.error("Unable to fetch data from Monday.com.")
            st.stop()



        # ------------------------------
        # Compute Business Metrics
        # ------------------------------

        total_work_orders = len(work_df)

        if "Execution Status" in work_df.columns:

            completed = work_df[work_df["Execution Status"] == "Completed"].shape[0]
            not_started = work_df[work_df["Execution Status"] == "Not Started"].shape[0]

        else:
            completed = 0
            not_started = 0


        metrics_context = f"""
        Operational Metrics:

        Total Work Orders: {total_work_orders}
        Completed: {completed}
        Not Started: {not_started}
        """


        # Ask AI
        answer = ask_agent(query + metrics_context, deals_df, work_df)


    # Store assistant message
    messages.append({"role": "assistant", "content": answer})


    with st.chat_message("assistant"):
        st.markdown(answer)


    # ------------------------------
    # Data Quality Warning
    # ------------------------------

    missing_values = deals_df.isnull().sum().sum() + work_df.isnull().sum().sum()
