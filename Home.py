import streamlit as st
import json

with open("language_dictionary.json", "r", encoding="utf-8") as archivo:
    language_dictionary = json.load(archivo)

st.set_page_config(page_title="StudySum AI", page_icon=":book:", initial_sidebar_state="expanded")

first_col, second_col, third_col = st.columns([0.05, 0.15, 0.8])
flag = first_col.toggle(' ')
language, index = ("English", 1) if flag is False else ("Español", 0)
second_col.write(language)
third_col.title(":book: StudySum AI")
st.header(language_dictionary["header_main"][index])

st.info(language_dictionary["api_header_text"][index])

col1, col2 = st.columns([0.35, 0.65])
with col1.expander("#### [PDFs](https://studysumai.streamlit.app/PDFs)", expanded=True):
    st.write(language_dictionary["pdf_text"][index])

with col2.expander("#### [Excel/CSV](https://studysumai.streamlit.app/Excel-CSV)", expanded=True):
    st.write(language_dictionary["data_text"][index])

with col2.expander("#### [YouTube Videos](https://studysumai.streamlit.app/YoutubeVideos)", expanded=True):
    st.write(language_dictionary["yt_text"][index])

with st.expander("API Keys Info :key:"):
    st.info(language_dictionary["api_text"][index])

with st.expander(language_dictionary["consideration"][index]):
    st.info(language_dictionary["consideration_text"][index])

with st.expander(language_dictionary["models"][index]):
    st.info(language_dictionary["model_text"][index])

with st.expander(language_dictionary["limitations"][index]):
    st.warning(language_dictionary["limitations_text"][index])


st.sidebar.info(f"""{language_dictionary["contact"][index]}:            
- [LinkedIn](https://www.linkedin.com/in/kevinchavez24/)
- [GitHub](https://github.com/PyKev)
""")
