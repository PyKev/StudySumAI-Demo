import streamlit as st
from summary_model import generate_document, extract_text, summarization_chain
import time
from chat_model import get_response, ingest
import datetime
import json

from utils import llm_choice

with open("language_dictionary.json", "r", encoding="utf-8") as archivo:
    language_dictionary = json.load(archivo)

st.set_page_config(page_title="StudySum AI", page_icon=":book:", initial_sidebar_state="expanded")

# Header
first_col, second_col, third_col = st.columns([0.05, 0.15, 0.8])
flag = first_col.toggle(' ')
language, index = ("English", 1) if flag is False else ("Español", 0)
second_col.write(language)
third_col.title(language_dictionary["doc_title"][index])

# Setting model and api key options
model_name = st.sidebar.selectbox(language_dictionary["model_name"][index],
                                  ('GPT-3.5-turbo-16k', 'GPT-3.5-turbo-4k', 'Mistral-7b' ,'Falcon-7b'))

if model_name.startswith("GPT"):
    key = st.sidebar.text_input("OpenAI API Key:", placeholder="sk-XXXXXXXXXXXXXXX", type='password')
else:
    key = st.sidebar.text_input("Hugging Face API Key:", placeholder="hf_XXXXXXXXXXXXXXX", type='password')

llm = llm_choice(model_name, "api_key", 'llm')

uploaded_files = st.file_uploader(language_dictionary["doc_upload"][index], accept_multiple_files=True, type=["pdf"])
disabled_state = False if uploaded_files else True

# Showing the file with the maximum number of tokens
max_tokens = 0
max_tokens_file = ""
for file in uploaded_files:
    text_file = extract_text(file)
    num_tokens = llm.get_num_tokens(text_file)
    if num_tokens > max_tokens:
        max_tokens = num_tokens
        max_tokens_file = file.name

if max_tokens_file:
    st.info(language_dictionary["doc_info_token"][index].format(max_tokens_file=max_tokens_file, max_tokens=max_tokens))
else:
    st.info(language_dictionary["doc_no_files"][index])

# Setting document name
input_name_document = st.text_input(language_dictionary["doc_summary_name"][index])
date_time_format = datetime.datetime.now().strftime('%Y%m%d%H%M')
document_name_dt = f"Resumen-{date_time_format}" if language == "Español" else f"Summary-{date_time_format}"
document_name = document_name_dt if input_name_document == "" else input_name_document

# Optional summary features
input_feature = st.text_input(language_dictionary["extra_features"][index],
                              placeholder=language_dictionary["features_example"][index])

# Summary button
col_btn_1, col_btn_2 = st.columns([0.3, 0.7])
btn_summary = col_btn_1.button(language_dictionary["doc_summary"][index], disabled=disabled_state)

language_translated = "in Spanish" if language == "Español" else "in English"
buffer_pdf, buffer_word = None, None
if btn_summary:
    if key:
        try:
            with st.spinner(language_dictionary["wait_message"][index]):
                summary_text = summarization_chain(model_name, key, uploaded_files, language_translated, input_feature)
                buffer_pdf = generate_document(summary_text, document_name, ".PDF")
                buffer_word = generate_document(summary_text, document_name, ".DOCX")
            st.success(language_dictionary["doc_success"][index], icon="✅")
        except Exception as e:
            st.error(str(e))
            st.stop()
    else:
        st.error(language_dictionary["api_error"][index])

# Download Documents
if buffer_pdf is not None and buffer_word is not None:
    st.download_button(label=language_dictionary["doc_download"][index] + " " + "PDF",
                       data=buffer_pdf.getvalue(),
                       file_name=f"{document_name}" + ".pdf")
    st.download_button(label=language_dictionary["doc_download"][index] + " " + "Word",
                       data=buffer_word.getvalue(),
                       file_name=f"{document_name}" + ".docx")
    buffer_pdf.close()
    buffer_word.close()

# Chat implementation
if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    if key:
        try:
            with st.spinner(language_dictionary["wait_message"][index]):
                ingest(key, uploaded_files)
            st.success(language_dictionary["success_indexing_doc"][index])
            st.session_state.clicked = True
        except Exception as i:
            st.error(str(i))
            st.stop()
    else:
        st.error(language_dictionary["api_error"][index])


col_btn_2.button(language_dictionary["doc_chat"][index], on_click=click_button, disabled=disabled_state)

if st.session_state.clicked:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if st.button(language_dictionary["clean"][index]):
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input(language_dictionary["write_message"][index]):
        st.session_state.messages.append({"role": "user", "content": prompt})
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
        disabled_chat = False
        st.session_state.messages.append({"role": "assistant", "content": full_response})
