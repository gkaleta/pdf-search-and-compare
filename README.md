# PDF Similarity Search Application

This repository contains a Flask web application that allows users to upload PDF files, extract text content, generate embeddings using Azure OpenAI, index the embeddings in Azure Cognitive Search, and perform vector searches to find similar PDFs based on content.

## **Features**

- Upload PDFs and store them securely in Azure Blob Storage.
- Extract text content from PDFs.
- Generate embeddings using Azure OpenAI's Embedding API.
- Index documents and embeddings in Azure Cognitive Search.
- Perform semantic searches to find similar PDFs.
- Simple and intuitive web interface.

## **Setup Instructions**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/pdf-search-app.git
cd pdf-search-app
```

### **2. Set Up Azure Resources**

- Create a Storage Account, Cognitive Search, and Azure OpenAI resource in the Azure Portal.
- Set up environment variables in `config.py` or directly in the environment.

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Run the Application Locally**

```bash
python app.py
```

## **Usage**

- Upload PDFs and perform searches via the web interface.

## Architecture 
![image](https://github.com/user-attachments/assets/c3b68f55-d62d-42fd-b0ed-5189981ba9e7)


## **License**

MIT License.
