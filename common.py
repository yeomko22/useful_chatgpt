import random
import time

import openai
import streamlit as st


def print_streaming_message(message: str):
    placeholder = st.empty()
    cur_message = ""
    for chr_ in message:
        cur_message += chr_
        placeholder.markdown(f"{cur_message} ▌")
        time.sleep(random.randint(1, 2) / 100)
    placeholder.markdown(cur_message)


def print_streaming_response(response):
    message = ""
    placeholder = st.empty()
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            placeholder.markdown(message + "▌")
        else:
            break
    placeholder.markdown(message)
    return message


def write_page_config():
    st.set_page_config(page_title="chatGPT AI 서비스 개발", page_icon="🧠")


def request_chat_completion(messages, system_role=None):
    if system_role:
        messages = [{"role": "system", "content": system_role}] + messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        timeout=3
    )
    return response
