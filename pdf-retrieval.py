import os
import openai
import gradio as gr
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.document_loaders import DirectoryLoader
from langchain.chat_models import ChatOpenAI

# os.environ["OPENAI_API_KEY"] = ""
openai.api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0, model_name="gpt-4")

# Data Ingestion
pdf_loader = DirectoryLoader('/Users/shreyas.sk/Downloads/', glob="**/*.pdf")
# excel_loader = DirectoryLoader('./Reports/', glob="**/*.txt")
# word_loader = DirectoryLoader('./Reports/', glob="**/*.docx")

loaders = [pdf_loader]  # , excel_loader, word_loader]
documents = []
for loader in loaders:
    documents.extend(loader.load())

# Chunk and Embeddings
text_splitter = CharacterTextSplitter(chunk_size=2500, chunk_overlap=50)
documents = text_splitter.split_documents(documents)


embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

memory = ConversationSummaryMemory(
    llm=llm,
    output_key='answer',
    memory_key='chat_history',
    return_messages=True)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4, "include_metadata": True})

# Initialise Langchain - Conversation Retrieval Chain
qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, return_source_documents=True,
                                           memory=memory, chain_type="stuff", get_chat_history=lambda h: h)

# Front end web app
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
        return gr.update(value=""), history


    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(debug=True)
