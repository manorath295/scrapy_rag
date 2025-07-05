




from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def setup_and_run_rag_pipeline(question: str):
    # Load and structure documents
    loader = JSONLoader(
        file_path='output.json',
        jq_schema='.[].content',
        text_content=False
    )
    docs = loader.load()

    # Split documents into coherent chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)

    # Embeddings
    embedder = GoogleGenerativeAIEmbeddings(
        google_api_key="",
        model="models/text-embedding-004"
    )

    # Store in Qdrant
    vector_store = QdrantVectorStore.from_documents(
        documents=splits,
        url="http://localhost:6333",
        collection_name="chaidocs_collection",
        embedding=embedder,
    )

    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an assistant for question-answering tasks. Use the following context to answer. "
         "Be clear, accurate, and ask before proceeding to the next step.\n\n{context}\n\n"
         "if you not known about result then return i dont have context about this"
         "only return result if in store presnt "
         "Process: 1. Plan  2. Think  3. Output."
         "MUST DO Store the url and return the url from where you are giving result in docs"),
        ("human", "{input}")
    ])

    llm = ChatGoogleGenerativeAI(
        google_api_key="AIzaSyCnDPypbbYubsbpWC0k5F8M8Vbkya-RdvY",
        model="gemini-2.0-flash"
    )

    qa_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, qa_chain)

    return rag_chain.invoke({"input": question})['answer']
