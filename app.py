import streamlit as st
from bedrock_utils import query_knowledge_base, generate_response, valid_prompt

st.title("Bedrock Chat Application")

# Sidebar config
st.sidebar.header("Configuration")
model_id = st.sidebar.selectbox(
    "Select LLM Model", 
    [
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0"
    ]
)

kb_id = st.sidebar.text_input("Knowledge Base ID", "your-knowledge-base-id")

temperature = st.sidebar.select_slider(
    "Temperature", [i/10 for i in range(0, 11)], 0.2
)
top_p = st.sidebar.select_slider(
    "Top_P", [i/100 for i in range(1, 101)], 0.9
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Safety / Filtering check
    if valid_prompt(prompt, model_id):

        # --- Step 1: Retrieve from Knowledge Base ---
        kb_results = query_knowledge_base(prompt, kb_id)

        print("KB RESULTS: ", kb_results)


        # --- Step 2: Pass KB results into LLM ---
        response = generate_response(
            prompt=prompt,
            model_id=model_id,
            kb_context=kb_results,
            temperature=temperature,
            top_p=top_p
        )

    else:
        response = "Your request cannot be processed. Please ask a different question."

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
