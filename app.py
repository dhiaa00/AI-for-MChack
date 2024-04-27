from flask import Flask, request, jsonify
from flask import make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename  # for secure file uploads
import json
import PyPDF2
import requests
import os

from google.generativeai import genai  # Import the genai library
# GET api from .env file
genai.configure(api_key= os.getenv('GEMINI_API_KEY'))


app = Flask(__name__)
CORS(app, origins='*')  # Allow CORS requests from all origins (adjust for production)

# Route to handle uploaded PDF files
@app.route('/facturisation', methods=['POST', 'OPTIONS'])
def process_pdf():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:517s3")  # Replace with Express app URL
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
    else:
        # Check if a file is uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        # Securely get the uploaded file
        pdf_file = request.files['file']
        filename = secure_filename(pdf_file.filename)

        # Save the uploaded file (temporary location)
        pdf_file.save(f"uploads/{filename}")  # Create 'uploads' folder if it doesn't exist

        # Extract text from the PDF
        text = extract_pdf_text(f"uploads/{filename}")

        # **Interaction with Express App:**
        import requests

        # Replace with the URL of your Express app endpoint
        url = "http://localhost:5000/api/v1/files/all" 

        # Send a GET request
        response = requests.get(url)

        # Check for successful response (status code 200)
        if response.status_code == 200:
          # Parse the response content (JSON format assumed)
          data = response.json()
        else:
          print(f"Error fetching data: {response.status_code}")

        
        modal_data = send_text_to_express_app(text)  

        # Generate the bill text based on the modal data (assuming format from Express app)
        bill_text = generate_bill_text(modal_data)

        return jsonify({"bill_text": bill_text})  # Return generated bill text

def extract_pdf_text(pdf_path):
    """
    Extracts text from a PDF file using PyPDF2.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    with open(pdf_path, 'rb') as pdf_obj:
        pdf_reader = PyPDF2.PdfReader(pdf_obj)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def generate_bill_text(modal_data):
    """
    Generates a formatted bill text based on the modal data (replace with your logic).

    Args:
        modal_data (dict): Dictionary containing formatted bill information from Express app.

    Returns:
        str: Formatted bill text.
    """
    bill_text = f"""
    Company Name: {modal_data.get('company_name', '')}
    Bill Date: {modal_data.get('bill_date', '')}
    Due Date: {modal_data.get('due_date', '')}
    Total Amount: {modal_data.get('total_amount', '')}

    Line Item Details:
    {modal_data.get('line_items', '')}

    Tax Information:
    {modal_data.get('tax_information', '')}
    """

    return bill_text

# Function to send text to your Express app (replace with your implementation)
def send_text_to_express_app(text):
  """
  Sends extracted text to your Express app for processing and prepares prompt for Gemini API.

  Args:
      text (str): Extracted text from the PDF.

  Returns:
      dict: Modal data received from the Express app (modified with prompt for Gemini).
  """

  url = "http://localhost:5000/api/v1/extract-text"

  # Example payload to send to the Express app
  payload = {
      "text": text
  }

  # Send a POST request with the extracted text
  response = requests.post(url, json=payload)

  # Check for successful response (status code 200)
  if response.status_code == 200:
      # Parse the response content (JSON format assumed)
      modal_data = response.json()

      # **Prepare prompt for Gemini API based on modal_data**
      prompt = f"Fill in the following form based on the extracted information: {modal_data['form_data']}"
      modal_data['prompt'] = prompt

      print(modal_data)
      return modal_data
  else:
      print(f"Error fetching modal data: {response.status_code}")
      return {}

@app.route('/extract_key_elements', methods=['POST', 'OPTIONS'])
def process_pdf():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5000/file/company/1")

    else:
        # Check if a file is uploaded 
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        # Securely get the uploaded file
        pdf_file = request.files['file']
        filename = secure_filename(pdf_file.filename)

        # Save the uploaded file
        pdf_file.save(f"uploads/{filename}")  # Create 'uploads' folder if it doesn't exist

        # Extract text from the PDF
        text = extract_pdf_text(f"uploads/{filename}")

        # **Interaction with Express App:**
        import requests
        import requests
        import json
        import io
        import PyPDF2

        url = "http://localhost:5000/api/v1/get-another-pdf"  
        def extract_text_from_express_pdf(pdf_data):
          """
          Extracts text from the PDF data received from the Express app.

          Args:
            pdf_data (bytes): PDF data received from the Express app.

          Returns:
            str: Extracted text from the PDF.
          """
          pdf_file = io.BytesIO(pdf_data)
          pdf_reader = PyPDF2.PdfReader(pdf_file)
          text = ""
          for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
          return text

          return extracted_text

        response = requests.get(url)

        # Check for successful response (status code 200)
        if response.status_code == 200:
          # Assuming response.content contains the PDF data
          express_pdf_data = response.content
          express_pdf_text = extract_text_from_express_pdf(express_pdf_data)
          # Combine extracted text from both PDFs
          combined_text = f"{text}\n{express_pdf_text}"
        else:
          print(f"Error fetching PDF data from Express app: {response.status_code}")
          express_pdf_text = ""  # Set to empty string if error
          print(f"Error fetching PDF data from Express app: {response.status_code}")
          express_pdf_text = ""  # Set to empty string if error

        # **Process text with Gemini API**
        prompt = f"This document describes a workflow process. Identify the steps involved, their responsible parties, and the tasks associated with each step. Here's the extracted text: {text}\n {express_pdf_text}"  # Include both texts in the prompt

        # Configure Gemini API
        def process_extracted_data(data):
          """
          Process the extracted data and convert it to the desired workflow structure.

          Args:
            data (dict): Extracted data from Gemini.

          Returns:
            dict: Processed workflow data.
          """
          processed_data = {}  # Define the variable "processed_data"
          # Implement the processing logic here
          processed_data = {}
          for step in data['steps']:
            step_name = step['name']
            responsible_parties = step['responsible_parties']
            tasks = step['tasks']
            processed_data[step_name] = {
              'responsible_parties': responsible_parties,
              'tasks': tasks
            }
          return processed_data

        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        model = genai.GenerativeModel('gemini-pro')  # Create a GenerativeModel object
        response = model.generate_content(prompt)

        # Process the response from Gemini (assuming it's JSON)
        try:
          extracted_data = json.loads(response.text)  # Assuming response contains JSON
          workflow_data = process_extracted_data(extracted_data)  # Implement this function
        except json.JSONDecodeError as e:
          print(f"Error parsing Gemini response JSON: {e}")
          workflow_data = {}

        # You can now use the workflow_data for visualization or further processing

        return jsonify({"workflow_data": workflow_data})  # Return extracted workflow data

process_pdf()