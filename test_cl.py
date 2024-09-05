import requests

def test_upload_api():
    # Define the API endpoint and the file path
    api_url = 'http://127.0.0.1:5000/upload'
    pdf_file_path = 'C:/Users/Admin/Downloads/test-file.pdf'
    # Path to the sample PDF file
    chat_name = 'chat'

    # Open the PDF file and prepare the data for the POST request
    with open(pdf_file_path, 'rb') as file:
        files = {'file': (pdf_file_path, file, 'application/pdf')}
        data = {'chat_name': chat_name}

        # Send the POST request
        response = requests.post(api_url, files=files, data=data)

        # Print the response
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")

def test_query_api(question):
    # Define the API endpoint and the file path
    api_url = 'http://127.0.0.1:5000/query'

    # Path to the sample PDF file
    chat_name = 'chat'

    response = requests.post(api_url, data={"chat_name": chat_name, "question": question})

    # Print the response
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

# test_upload_api()
test_query_api("Find the skills relevant to data science")
