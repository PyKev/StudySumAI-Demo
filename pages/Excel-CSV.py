import streamlit as st
from utils import llm_choice
import json
import time
import pandas as pd
from langchain.agents import create_pandas_dataframe_agent, AgentType

with open("language_dictionary.json", "r", encoding="utf-8") as archivo:
    language_dictionary = json.load(archivo)

st.set_page_config(page_title="StudySum AI", page_icon=":book:", initial_sidebar_state="expanded")

# Header
first_col, second_col, third_col = st.columns([0.05, 0.15, 0.8])
flag = first_col.toggle(' ')
language, index = ("English", 1) if flag is False else ("Español", 0)
second_col.write(language)
third_col.title(language_dictionary["data_title"][index])

# Setting model and api key options
model_name = st.sidebar.selectbox(language_dictionary["model_name"][index],
                                  ('GPT-3.5-turbo-4k', 'GPT-3.5-turbo-16k'))
if model_name.startswith("GPT"):
    key = st.sidebar.text_input("OpenAI API Key:", placeholder="sk-XXXXXXXXXXXXXXX", type='password')
else:
    key = st.sidebar.text_input("Hugging Face API Key:", placeholder="hf_XXXXXXXXXXXXXXX", type='password')

uploaded_data_files = st.file_uploader(language_dictionary["data_upload"][index], type=["xlsx", "csv"])
disabled_state = True
df = None

if uploaded_data_files:
    file_extension = uploaded_data_files.name.split(".")[-1].lower()
    if file_extension == "xlsx":
        df = pd.read_excel(uploaded_data_files, engine='openpyxl')
    elif file_extension == "csv":
        df = pd.read_csv(uploaded_data_files, encoding='ISO-8859-1')
    if df is not None:
        st.write(df)
        if key:
            llm = llm_choice(model_name, key, "data")
            agent = create_pandas_dataframe_agent(llm=llm, df=df, max_iterations=3,
                                                  max_execution_time=20, agent_type=AgentType.OPENAI_FUNCTIONS)
            disabled_state = False
        else:
            st.error(language_dictionary["api_error"][index])
    else:
        st.error(language_dictionary["data_error"][index])

if "messages3" not in st.session_state:
    st.session_state.messages3 = []
if st.button(language_dictionary["clean"][index], disabled=disabled_state):
    st.session_state.messages3 = []
for message in st.session_state.messages3:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input(language_dictionary["write_message"][index], disabled=disabled_state):
    st.session_state.messages3.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            assistant_response = agent.run(prompt)
        except Exception as e:
            st.error(str(e))
            st.stop()
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    disabled_chat = False
    st.session_state.messages3.append({"role": "assistant", "content": full_response})
