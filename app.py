from flask import Flask, request, jsonify
from firebase_config import db
from pinecone_config import create_pinecone_index_if_not_exists
from gemini_config import get_gemini_response, get_embeddings
from PyPDF2 import PdfReader
import io
import time

app = Flask(__name__)


def validate_question(question):
    # Implement checks for relevance, language, etc.
    if not question.strip() or len(question) < 5:
        return False, "Question is too short or empty."
    return True, ""


@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files or 'chat_name' not in request.form:
        return jsonify({"error": "Please provide a PDF file and a chat_name"}), 400

    file = request.files['file']
    chat_name = request.form['chat_name']
    
    # Extract text from PDF
    pdf_reader = PdfReader(io.BytesIO(file.read()))
    document_text = "".join([pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))])

    index = create_pinecone_index_if_not_exists(chat_name)

    # Index document with Pinecone
    for idx, chunk in enumerate(document_text.splitlines()):
        vector = get_embeddings(chunk)
        index.upsert([{
            "id": chat_name + str(idx), 
            "values": vector,
            "metadata": {"raw": chunk}}])

    # Store metadata in Firebase
    db.collection("documents").document(chat_name).set({
        "index_name": chat_name
    })

    return jsonify({"message": "Document uploaded and indexed successfully"}), 200

@app.route('/query', methods=['POST'])
def query_document():
    if 'chat_name' not in request.form or 'question' not in request.form:
        return jsonify({"error": "Please provide a chat_name and a question"}), 400

    chat_name = request.form.get('chat_name')
    question = request.form.get('question')
    
    # Validate question
    is_valid, error_message = validate_question(question)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    # Retrieve document index from Firebase
    doc_ref = db.collection("documents").document(chat_name)
    doc = doc_ref.get()
    if not doc.exists:
        return jsonify({"error": "Document not found"}), 404

    index_name = doc.to_dict().get('index_name')
    index = create_pinecone_index_if_not_exists(index_name)
    query_result = index.query(vector=get_embeddings(question), top_k=2, include_metadata=True)

    prompt = f"""
    Use the data below to answer the question: ```{question}```
    
    ### Data
    {query_result}
    """
    print(prompt)
    return jsonify({"answer": get_gemini_response(prompt)}), 200

