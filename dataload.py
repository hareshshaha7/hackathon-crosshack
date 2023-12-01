from azure.identity import EnvironmentCredential
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import AzureChatOpenAI
from langchain.document_loaders import Docx2txtLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus

load_dotenv()


# Load data into the loader
def load_data(urls):
    # Use the WebBaseLoader to load specified web pages into documents
    # loader = WebBaseLoader(urls)
    # loader = UnstructuredURLLoader(urls=urls)
    loader = Docx2txtLoader("data/DataSource.docx")
    print("Data Loading...Started...✅✅✅")
    data = loader.load()
    return data


# Split the documents into smaller chunks
def split_data(data):
    chunk_size = 1000
    chunk_overlap = 100
    separators = ["\n\n", "\n", "(?<=\. )", " ", "", '.', ',']
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )
    print("Text Splitter...Started...✅✅✅")
    tokens = splitter.split_documents(data)
    return tokens


# Set your Azure AD instance options
api_base = "https://cog-sandbox-dev-eastus2-001.openai.azure.com/"
api_type = "azure_ad"
api_version = "2023-03-15-preview"
embeddings_deployment = "text-embedding-ada-002-blue"
embeddings_model = "text-embedding-ada-002"
llm_deployment = "gpt-35-turbo-blue"

credential = EnvironmentCredential()
access_token = credential.get_token("https://cognitiveservices.azure.com/.default")

# Define embeddings
embeddings = OpenAIEmbeddings(
    openai_api_base=api_base,
    openai_api_type=api_type,
    openai_api_key=access_token.token,
    openai_api_version=api_version,
    deployment=embeddings_deployment,
    model=embeddings_model,
    chunk_size=16,
)


def get_db(tokens):
    # Embed chunks and load them into the vector store
    print("Embedding Vector Started Building...✅✅✅")
    db = Milvus.from_documents(tokens, embeddings)
    return db


# Define LLM
llm = AzureChatOpenAI(
    openai_api_base=api_base,
    openai_api_version=api_version,
    openai_api_type=api_type,
    openai_api_key=access_token.token,
    deployment_name=llm_deployment,
)


# Use QA Chain (which combines llm and db) to answer questions about the transcript
def get_chain(db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever()
    )
    return qa_chain
