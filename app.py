# app.py
from flask import Flask, render_template, request, redirect, url_for
from config import Config
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    VectorField,
    VectorSearch,
    VectorSearchAlgorithmConfiguration
)
import openai
import PyPDF2

app = Flask(__name__)
app.config.from_object(Config)

# Configure Azure clients
blob_service_client = BlobServiceClient.from_connection_string(
    app.config['AZURE_STORAGE_CONNECTION_STRING']
)
container_name = 'pdf-container'
container_client = blob_service_client.get_container_client(container_name)

search_client = SearchClient(
    endpoint=f"https://{app.config['SEARCH_SERVICE_NAME']}.search.windows.net/",
    index_name=app.config['SEARCH_INDEX_NAME'],
    credential=app.config['SEARCH_API_KEY']
)

index_client = SearchIndexClient(
    endpoint=f"https://{app.config['SEARCH_SERVICE_NAME']}.search.windows.net/",
    credential=app.config['SEARCH_API_KEY']
)

openai.api_type = app.config['OPENAI_API_TYPE']
openai.api_base = app.config['OPENAI_API_BASE']
openai.api_version = app.config['OPENAI_API_VERSION']
openai.api_key = app.config['OPENAI_API_KEY']

# Ensure the container exists
try:
    container_client.create_container()
except Exception:
    pass

# Ensure the search index exists
def create_search_index():
    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SimpleField(name="file_name", type="Edm.String", filterable=True, sortable=True),
        SimpleField(name="content", type="Edm.String"),
        VectorField(
            name="embedding",
            dimensions=1536,
            vector_search_configuration="default"
        )
    ]

    vector_search = VectorSearch(
        algorithm_configurations=[
            VectorSearchAlgorithmConfiguration(
                name="default",
                algorithm="hnsw"
            )
        ]
    )

    index = SearchIndex(
        name=app.config['SEARCH_INDEX_NAME'],
        fields=fields,
        vector_search=vector_search
    )

    if app.config['SEARCH_INDEX_NAME'] in index_client.list_index_names():
        index_client.delete_index(app.config['SEARCH_INDEX_NAME'])

    index_client.create_index(index)

create_search_index()

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            blob_client = container_client.get_blob_client(uploaded_file.filename)
            blob_client.upload_blob(uploaded_file.read(), overwrite=True)
            process_pdf(uploaded_file.filename)
        return redirect(url_for('index'))
    else:
        return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        query_embedding = generate_embeddings(query)
        vector_query = {
            "value": query_embedding,
            "fields": "embedding",
            "k": 5
        }
        results = search_client.search(
            search_text="",
            vectors=[vector_query],
            select=["file_name", "content"]
        )
        return render_template('search.html', results=results)
    else:
        return redirect(url_for('index'))

# Helper functions
def process_pdf(file_name):
    # Download PDF from Blob Storage
    blob_client = container_client.get_blob_client(file_name)
    downloader = blob_client.download_blob()
    pdf_bytes = downloader.readall()

    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(pdf_bytes)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Generate embedding
    embedding = generate_embeddings(text)

    # Upload to Azure Cognitive Search
    doc = {
        'id': file_name,
        'file_name': file_name,
        'content': text,
        'embedding': embedding
    }
    search_client.upload_documents(documents=[doc])

def generate_embeddings(text):
    response = openai.Embedding.create(
        input=text,
        engine=app.config['OPENAI_EMBEDDING_ENGINE']
    )
    return response['data'][0]['embedding']

if __name__ == '__main__':
    app.run(debug=True)
