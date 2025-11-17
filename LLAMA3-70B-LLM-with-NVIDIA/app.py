from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import os


st.set_page_config(
    page_title="Code Pilot ChatApp",
    page_icon="🌟",
    layout="centered"
)

st.title("AI🌟 Code Pilot ChatApp 🤖")


if "messages" not in st.session_state:
    st.session_state.messages = []


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)


def stream_chat(user_input):
    try:
        messages = [{"role": "user", "content": user_input}]

        response_container = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=messages,
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )

        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response + "▌")

        response_container.markdown(full_response)
        return full_response

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "I apologize, but I encountered an error. Please try again."



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What would you like to know?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = stream_chat(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
