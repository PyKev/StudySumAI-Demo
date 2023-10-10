from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
import time
from PyPDF2 import PdfReader
import streamlit as st


def extract_text(file) -> str:
    """
    Extracts the text of a given PDF file.

    :param file: Uploaded file
    :return: Text of the file
    """
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    text = text.replace('\t', ' ')
    return text


def llm_choice(llm_name: str, key: str, mode: str):
    """
    Chooses the LLM model, available models: 'GPT-3.5-turbo-4k', 'GPT-3.5-turbo-16k', 'Falcon-7b'

    :param llm_name: Chosen model name
    :param key: OpenAI or HuggingFace key
    :param mode: 'sum' for summarization task, 'chat' for chat task, 'data' for Excel or CSV docs, 'llm' for only llm
    :return: Returns either the LLM alone or the LLM along with the context_length, depending on the mode. The chat task does not require the context_length since only summarization handles long text.
    """
    try:
        models = {
            "GPT-3.5-turbo-4k": ["gpt-3.5-turbo", 4097],
            "GPT-3.5-turbo-16k": ["gpt-3.5-turbo-16k", 16385],
            "Mistral-7b": ["mistralai/Mistral-7B-Instruct-v0.1", 8000],
            "Falcon-7b": ["tiiuae/falcon-7b-instruct", 1200]
        }
        temperature_gpt, temperature_hf = (0, 0.1) if mode == "sum" or mode == "data" else (0.5, 0.5)
        model_name = models[llm_name][0]
        context_length = models[llm_name][1]
        if model_name.startswith("gpt"):
            llm = ChatOpenAI(temperature=temperature_gpt, model_name=model_name, openai_api_key=key)
        else:
            llm = HuggingFaceHub(
                repo_id=model_name, model_kwargs={"temperature": temperature_hf, "max_new_tokens": 300},
                huggingfacehub_api_token=key
            )
        if mode == "sum":
            return llm, context_length
        else:
            return llm
    except Exception as e:
        st.error(str(e))
        st.stop()


map_prompt = """
You will be given a single part of a {matter}. This section will be enclosed in triple backticks (```)
Your goal is to write a very short easy to understand summary {lang}.{features}
```{text}```
"""

combine_prompt = """
You will be given a series of summaries of a {matter}. The summaries will be enclosed in triple backticks (```)
Your goal is to write a detailed easy to understand summary of the summaries {lang}.{features}
```{text}```
"""


def handle_long_text(llm, context_length: int, text: str, lang: str, matter: str, features: str) -> str:
    """
    Returns the summary of a very large PDF document.
    Splits the text of the PDF into chunks, with each piece being processed to obtain a summary of them.
    A waiting time of 60 seconds has been added after every 3 chunks to avoid the error of making too many API calls.
    Then, each summary is taken, and the summary of these summaries is returned.

    :param llm: LLM model chosen before
    :param context_length: The number of tokens a language model can process at once
    :param text: Text of the large PDF document
    :param lang: Chosen language
    :param matter: 'text' if it is a document summarization, 'data about a YouTube video transcription' if it is a YouTube video summarization
    :param features: Additional features for the summaries
    :return: Summary of the summaries of the large PDF document
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=context_length*3.5)
    docs = text_splitter.create_documents([text])
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "lang", "matter", "features"])
    combine_prompt_template = PromptTemplate(template=combine_prompt,
                                             input_variables=["lang", "matter", "text", "features"])
    map_chain = load_summarize_chain(llm=llm, chain_type="stuff", prompt=map_prompt_template)
    summary_list = []
    for index, doc in enumerate(docs):
        chunk_summary = map_chain.run({'text': [doc], 'matter': matter, 'lang': lang,
                                       'input_documents': [doc], 'features': features})
        if (index + 1) % 3 == 0:
            if context_length != 1200:
                time.sleep(61)
        summary_list.append(chunk_summary)
    summaries = "\n".join(summary_list)
    summaries = Document(page_content=summaries)

    reduce_chain = load_summarize_chain(llm=llm, chain_type="stuff", prompt=combine_prompt_template)
    return reduce_chain.run({'lang': lang, 'matter': matter,
                             'text': [summaries], 'input_documents': [summaries], 'features': features})
