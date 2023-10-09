import streamlit as st
from summary_model import youtube_summarization, get_youtube_transcript
import time
from chat_model import get_response, ingest
import json
import tiktoken
with open("language_dictionary.json", "r", encoding="utf-8") as archivo:
    language_dictionary = json.load(archivo)

st.set_page_config(page_title="StudySum AI", page_icon=":book:", initial_sidebar_state="expanded")

# Header
first_col, second_col, third_col = st.columns([0.05, 0.15, 0.9])
flag = first_col.toggle(' ')
language, index = ("English", 1) if flag is True else ("Español", 0)
language_translated = "in Spanish" if language == "Español" else "in English"
second_col.write(language)
third_col.title(language_dictionary["yt_title"][index])

# Setting model and api key options
model_name = st.sidebar.selectbox(
    language_dictionary["model_name"][index], ('GPT-3.5-turbo-16k', 'GPT-3.5-turbo-4k', 'Falcon-7b'))
if model_name.startswith("GPT"):
    key = st.sidebar.text_input("OpenAI API Key:", placeholder="sk-XXXXXXXXXXXXXXX", type='password')
else:
    key = st.sidebar.text_input("Hugging Face API Key:", placeholder="hf_XXXXXXXXXXXXXXX", type='password')

input_link = st.text_input("Youtube link:", placeholder="https://www.youtube.com/watch?XXXXXXXXX")
disabled_state_link = True

# Showing the number of tokens of the video
if input_link:
    yt_transcript_s = get_youtube_transcript(input_link)
    if yt_transcript_s != "fail":
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(yt_transcript_s))
        st.info(language_dictionary["yt_token_message"][index]+str(num_tokens)+" tokens")
        disabled_state_link = False
    else:
        st.error(language_dictionary["yt_error"][index])
else:
    st.info(language_dictionary["yt_link_error"][index])

# Summary button
col_btn_1, col_btn_2 = st.columns([0.35, 0.65])
btn_summary_yt = col_btn_1.button(language_dictionary["yt_summary"][index], disabled=disabled_state_link)
if btn_summary_yt:
    if key:
        try:
            with st.spinner(language_dictionary["wait_message"][index]):
                response_yt = youtube_summarization(yt_transcript_s, model_name, key, language_translated)
            st.write(response_yt)
        except Exception as y:
            st.error(str(y))
            st.stop()
    else:
        st.error(language_dictionary["api_error"][index])

# Chat implementation
if 'clicked2' not in st.session_state:
    st.session_state.clicked2 = False


def click_button():
    if input_link:
        if key:
            yt_transcript_c = get_youtube_transcript(input_link)
            if yt_transcript_c != "fail":
                try:
                    with st.spinner(language_dictionary["wait_message"][index]):
                        ingest(key, video_text=yt_transcript_c)
                    st.success(language_dictionary["success_indexing_yt"][index])
                    st.session_state.clicked2 = True
                except Exception as iy:
                    st.error(str(iy))
                    st.stop()
            else:
                st.error(language_dictionary["yt_error"][index])
        else:
            st.error(language_dictionary["api_error"][index])
    else:
        st.error(language_dictionary["yt_link_error"][index])


col_btn_2.button(language_dictionary["yt_chat"][index], on_click=click_button, disabled=disabled_state_link)

if st.session_state.clicked2:
    if "messages2" not in st.session_state:
        st.session_state.messages2 = []
    if st.button(language_dictionary["clean"][index]):
        st.session_state.messages2 = []
    for message in st.session_state.messages2:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input(language_dictionary["write_message"][index]):
        st.session_state.messages2.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = get_response(model_name, key, prompt)
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages2.append({"role": "assistant", "content": full_response})
