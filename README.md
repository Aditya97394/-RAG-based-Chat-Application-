# RAG-Based Chat APIs using Google Gemini, Pinecone, and Firebase


# This project demonstrates how to build Retrieval-Augmented Generation (RAG)-based chat APIs using Google Gemini for generative AI, Pinecone for vector search, and Firebase for document storage. The APIs allow users to upload PDF documents, index them for efficient querying, and retrieve responses to natural language questions based on the document content.


# Table of Contents
1.Prerequisites
2.Installation
3.Environment Variables
4.Running the Application
5.API Endpoints
6.Code Explanation

# Prerequisites
Ensure you have the following tools and services:

1.Python 3.7+ installed.
2.Google API key for Gemini (Generative AI API).
3.Pinecone API key for vector search.
4.Firebase project set up with Firestore enabled.
5.firebase-adminsdk.json service account file from Firebase.
6.Basic knowledge of REST APIs, PDF handling, and vector-based search.

# Installation
Clone the repository:


1.git clone <repository_url>

cd <project_directory>



2.python3 -m venv venv
 -`venv\Scripts\activate`

# .Install the dependencies:
pip install -r requirements.txt
Place the Firebase service account credentials (firebase-adminsdk.json) in the project directory.

# .Environment Variables
Create a .env file in the root directory and set the following environment variables:

-GOOGLE_API_KEY=your-google-api-key
-PINECONE_API_KEY=your-pinecone-api-key

# API Endpoints

1. /upload - Upload a PDF and index it
-Method: POST
-Description: Upload a PDF document and index its content in Pinecone for future queries.
# Form Data:
-file: PDF file to be uploaded.
-chat_name: A unique identifier for the chat/document.

# Response:
Success: { "message": "Document uploaded and indexed successfully" }
Error: { "error": "Error message" }

2. /query - Query a document for an answer 
Method: POST
-Description: Query a document by asking a question. The API retrieves the most relevant document chunks from -Pinecone and uses Google Gemini to generate a response.

# Form Data:
-chat_name: The name of the chat/document to be queried.
-question: The natural language question.

# Response:
Success: { "answer": "Generated response based on document content" }
Error: { "error": "Error message" }

# Code Explanation
Main Flask Application (app.py)
-validate_question(question): Checks the validity of a question (e.g., length, relevance).

# /upload:

-Extracts text from an uploaded PDF using PyPDF2.
-Indexes the text into Pinecone, breaking it into smaller chunks.
-Stores metadata in Firebase Firestore.

# /query:
-Retrieves the document index from Firebase.
-Queries Pinecone with the embeddings of the user's question.
-Uses Google Gemini to generate a response from the most relevant document chunks

# Firebase Configuration (firebase_config.py)
-Initializes Firebase Firestore using the service account credentials stored in firebase-adminsdk.json.

# Google Gemini Configuration (gemini_config.py)
-Handles calls to Google Generative AI (Gemini) for both embeddings and response generation.

# Pinecone Configuration (pinecone_config.py)
Creates and manages Pinecone indexes. It either creates a new index or retrieves an existing one.

# Testing
The project includes a test client (test_cl.py) to manually test the API endpoints.

# Test Upload API:
This function uploads a PDF to the /upload endpoint:

# test_upload_api()
Test Query API:
This function sends a question to the /query endpoint and retrieves a response:

# test_query_api("Find the skills relevant to data science")