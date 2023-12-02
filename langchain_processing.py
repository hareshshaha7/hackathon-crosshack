from azure.identity import EnvironmentCredential
from dotenv import load_dotenv
from dotenv.main import get_key
from langchain.chains import RetrievalQA
from langchain.chat_models import AzureChatOpenAI
from langchain.document_loaders import Docx2txtLoader, UnstructuredURLLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus

load_dotenv()

# Set your Azure AD instance options
api_base = get_key(dotenv_path=".env", key_to_get="AZURE_API_BASE")
api_type = get_key(dotenv_path=".env", key_to_get="AZURE_API_TYPE")
api_version = get_key(dotenv_path=".env", key_to_get="API_VERSION")
embeddings_deployment = get_key(dotenv_path=".env", key_to_get="AZURE_EMBEDDINGS_DEPLOYMENT")
embeddings_model = get_key(dotenv_path=".env", key_to_get="AZURE_EMBEDDINGS_MODEL")
llm_deployment = get_key(dotenv_path=".env", key_to_get="AZURE_LLM_DEPLOYMENT")

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

# Define LLM
llm = AzureChatOpenAI(
    openai_api_base=api_base,
    openai_api_version=api_version,
    openai_api_type=api_type,
    openai_api_key=access_token.token,
    deployment_name=llm_deployment,
)

# Get existing collection from Milvus
vector_db = Milvus(
    embedding_function=embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
    collection_name="sample"
)


# Load data into the loader
def load_file(file_path):
    print("Data Loading...Started...✅✅✅")
    # Use the WebBaseLoader to load specified web pages into documents
    loader = Docx2txtLoader(file_path)

    data = loader.load()
    return data


# Load data into the loader
def load_url(urls):
    print("Data Loading...Started...✅✅✅")
    # # Use the WebBaseLoader to load specified web pages into documents
    # loader = WebBaseLoader(urls)
    loader = UnstructuredURLLoader(urls=urls)

    data = loader.load()
    return data


# Split the documents into smaller chunks
def split_data(data):
    chunk_size = 1000
    chunk_overlap = 100
    separators = ["\n\n", "\n", "(?<=\. )", " ", "", '.', ',']
    print("Text Splitter...Started...✅✅✅")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )

    tokens = splitter.split_documents(data)
    return tokens


def store_data(tokens):
    print("Embedding Vector Started Building...✅✅✅")
    vector_db.add_documents(
        documents=tokens
    )


def get_answer(query):
    print("Retrieving answer from vector chain...✅✅✅")
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_db.as_retriever()
    )

    return chain({"query": query})
