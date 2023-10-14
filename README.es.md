# StudySum AI - Resúmenes y Chat con PDFs, Excel/CSV y Videos de YouTube 📚

Esta aplicación te permite resumir y chatear con tus documentos PDF y videos de YouTube. Para aprovechar al máximo esta aplicación, necesitas una API key de OpenAI y, opcionalmente, una API key de HuggingFace. Aquí te muestro cómo obtenerlas:

- **API key de OpenAI:** Regístrate en [OpenAI](https://openai.com/) para obtener una API key. Al crear tu cuenta por primera vez, recibirás $5 de crédito.

- **Access Token de HuggingFace:** Regístrate en [HuggingFace](https://huggingface.co/), ve a 'Settings' y luego a 'Access Tokens' para obtener tu clave.

## Funcionalidades 🔧

Esta app ofrece dos funcionalidades principales:

### PDFs:

1. **Resumir:** Carga tus archivos PDF, selecciona el modelo que desees y proporciona tu clave de API. Luego, puedes generar un resumen descargable en PDF o Word con opciones de personalización.

2. **Chatear:** Indexa tus PDFs en un Vector Store y permite consultas mediante un chat. Esto facilita la búsqueda y recuperación de información relevante.

### YouTube Videos:

1. **Resumir:** Inserta el enlace de un video de YouTube, elige el modelo y proporciona tu clave de API. La aplicación generará un resumen del video que se muestra en la página como texto.

2. **Chatear:** Indexa el video en el Vector Store y habilita el chat para realizar consultas relacionadas con el contenido del video.

### Excel/CSV:

1. **Chatear:** Sube tu archivo y habilitará un chat para que puedas hacer preguntas sobre él.
   
Un 'Vector Store' actúa como una base de datos que almacena representaciones vectoriales de texto, lo que permite realizar búsquedas de similitud.

## Tecnologías usadas 👨‍💻:
### Frameworks 🛠️
- Langchain: Framework que permite simplificar la creación de aplicaciones utilizando grandes modelos de lenguaje (LLM).
  - Cadenas utilizadas: LLMChain, RetrievalQA, load_summarize_chain
  - Vector Store: FAISS
  - Embeddings: text-embedding-ada-002
  - Memoria: ConversationBufferWindowMemory
  - Agente: create_pandas_dataframe_agent

- StreamLit: Framework de desarrollo de front-end que permite crear aplicaciones web interactivas de manera sencilla y rápida.
### Modelos 🤖

Este proyecto utiliza 3 modelos de lenguaje grandes (LLMs) para procesar contenido:

1. Modelo de pago: Requiere una clave de API de OpenAI.
   - **GPT-3.5 Turbo:** Ofrece los mejores resultados, cuenta con dos variantes con límites de tokens de 4096 y 16,384. Puedes elegir el modelo según la longitud de tu texto.

2. Modelos de código abierto: Requieren un Access Token de HuggingFace.
   - **Mistral-7b-Instruct:** Considerado el mejor modelo de 7B hasta la fecha, proporciona respuestas aceptables, pero no alcanza el nivel de GPT, aunque tiene un limite de 8000 tokens.
   - **Falcon-7b-Instruct:** Tiene un límite de tokens más bajo, no funciona tan bien como GPT y Mistral, además proporciona resultados regulares con textos de alrededor de 1200 tokens.

- La aplicación te mostrará cuál de tus archivos tiene el mayor número de tokens para ayudarte a decidir que modelo usar.
- Cuando un texto supera el límite de tokens permitido, el código divide el contenido en partes más pequeñas y genera un resumen de los resúmenes utilizando la técnica de map_reduce. Se recomienda utilizar el modelo GPT-3.5 Turbo de 16k tokens para obtener mejores resultados en textos extensos.

### Generación y manipulación de documentos 📄
Cuando se sube un archivo, el sistema genera resúmenes y almacena temporalmente los documentos resultantes en búferes que se cierran y pierden su valor después de haberlos descargado.

- PyPDF: Para la extracción del texto del PDF.
- ReportLab: Para generar documentos PDF.
- Python-docx: Para generar documentos Word.

## Consideraciones 📍

- Se recomienda elegir el modelo que mejor se adapte al número de tokens de tu archivo o video.

- La aplicación está disponible en español e inglés, lo que significa que los resúmenes generados estarán en el idioma que elijas.

- El chatbot solo conserva la información de la última pregunta que le hagas, a excepción del chatbot de Excel/CSV que no tiene memoria implementada.

- Si deseas agregar más documentos después de utilizar la función de chat, asegúrate de eliminar los documentos previamente indexados y cargar los nuevos para evitar duplicaciones y no gastar créditos innecesariamente.

- Si deseas chatear con más videos posteriormente, simplemente ingresa la URL del nuevo video y presiona "Chatear"; de esta manera, el chatbot tendrá información de todos los videos que ingreses a partir de ese momento.

## Limitaciones ⚠️

- Para que el chat funcione correctamente, es necesario ingresar tu clave de OpenAI, ya que los embeddings se generan mediante el modelo 'text-embedding-ada-002'. Existe la alternativa gratuita 'HuggingFaceInstructEmbeddings', pero su procesamiento es más lento, requiere una mayor cantidad de recursos y no se ha agregado a este proyecto.
  - Si bien el proceso de indexación se realiza con una clave de API de OpenAI, una vez indexado, puedes utilizar un modelo de código abierto para obtener respuestas.
- Ten en cuenta que pueden surgir errores de procesamiento si el texto es demasiado extenso y se elige un modelo con un límite bajo de tokens.
