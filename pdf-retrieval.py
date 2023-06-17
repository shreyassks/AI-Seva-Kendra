import gradio as gr
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0.1, model_name="gpt-4")

# Data Ingestion
pdf_loader = PyPDFDirectoryLoader('static/')

documents = pdf_loader.load()

# Chunk and Embeddings
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(documents, embeddings, persist_directory="db")
vectorstore.persist()
vectordb = Chroma(persist_directory="db", embedding_function=embeddings)

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=850,
    output_key='answer',
    memory_key='chat_history',
    return_messages=True)

retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3})

# Initialise Langchain - Conversation Retrieval Chain
qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory,
                                           get_chat_history=lambda h: h,
                                           chain_type="stuff")

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    chat_history = []


    def user(user_message, history):
        # Get response from QA chain
        response = qa({"question": user_message, "chat_history": history})
        # Append user message and response to chat history
        history.append((user_message, response["answer"]))
        # print(type(history[0]))
        return gr.update(value=""), history


    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(debug=True)