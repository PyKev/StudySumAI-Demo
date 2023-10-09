# StudySum AI - Summaries and Chat with PDFs and YouTube Videos 📚

This application allows you to summarize and chat with your PDF documents and YouTube videos. To make the most of this application, you need an API key from OpenAI and, optionally, an API key from HuggingFace. Here's how to get them:

- **OpenAI API Key:** Sign up on [OpenAI](https://openai.com/) to get an API key. When creating your account for the first time, you will receive $5 in credit.

- **HuggingFace API Key:** Sign up on [HuggingFace](https://huggingface.co/), go to 'Settings,' and then 'Access Tokens' to obtain your key.

## Features 🔧

This app offers two main functionalities:

### PDFs:

1. **Summarize:** Upload your PDF files, select the desired model, and provide your API key. You can then generate a downloadable summary in PDF or Word format with customization options.

2. **Chat:** Index your PDFs in a Vector Store and allow queries through a chat. This makes it easy to search for and retrieve relevant information.

### YouTube Videos:

1. **Summarize:** Insert the link to a YouTube video, choose the model, and provide your API key. The application will generate a summary of the video displayed on the page as text.

2. **Chat:** Index the video in the Vector Store and enable chat to make queries related to the video's content.

A 'Vector Store' acts as a database that stores vector representations of text, enabling similarity searches.

## Technologies Used 👨‍💻
### Frameworks🛠 🛠️
- Langchain: A framework that simplifies the creation of applications using large language models (LLMs).
  - Used Chains: LLMChain, RetrievalQA, load_summarize_chain
  - Vector Store: FAISS
  - Embeddings: text-embedding-ada-002
  - Memory: ConversationBufferWindowMemory

- StreamLit: A front-end development framework that allows for easy and fast creation of interactive web applications.

### Models 🤖

This project uses two language models (LLMs) to process content:

1. **GPT-3.5 Turbo:** Offers two variants with token limits of 4096 and 16,384. You can choose the model based on your text's length. The application will show you which of your files has the highest number of tokens to help you decide.

2. **Falcon-7b:** This model is free with your HuggingFace API key but has a lower token limit, ideal for summarizing shorter texts, usually around 1200 tokens.

When a text exceeds the allowed token limit, the code divides the content into smaller parts and generates summaries of the summaries using the map_reduce technique. It is recommended to use the 16k token GPT-3.5 Turbo model for better results on longer texts.

### Document Generation and Manipulation 📄
When a file is uploaded, the system generates summaries and temporarily stores the resulting documents in buffers that are closed and lose their value after downloading.

- PyPDF and PyPDF2: For text extraction from PDFs.
- ReportLab: For generating PDF documents.
- Python-docx: For generating Word documents.

## Considerations 📍

- It is recommended to choose the model that best fits the token count of your file or video.

- The application is available in both Spanish and English, which means the generated summaries will be in the language you choose.

- The chatbot only retains information from the last question you ask.

- If you want to add more documents after using the chat function, make sure to remove previously indexed documents and load the new ones to avoid duplication and unnecessary credit usage.

- If you want to chat with more videos later, simply enter the URL of the new video and press "Chat." This way, the chatbot will have information about all the videos you input from that point onward.

## Limitations ⚠️

- To make the chat work correctly, it is necessary to input your OpenAI key since embeddings are generated using the 'text-embedding-ada-002' model. There is a free alternative, 'HuggingFaceInstructEmbeddings,' but it processes more slowly, requires more resources, and has not been added to this project.
