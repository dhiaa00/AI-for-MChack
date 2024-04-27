````
# PDF Facturisation and Workflow Extraction

This repository contains a Flask application that provides endpoints to process PDF files for facturisation and extract key workflow elements. The application utilizes Flask for handling HTTP requests, PyPDF2 for PDF text extraction, and requests for interacting with other services.

## Features

1. **Facturisation Endpoint:** Accepts PDF files, extracts text, interacts with an Express app to obtain modal data, generates a bill text based on the modal data, and returns the generated bill text.

2. **Workflow Extraction Endpoint:** Accepts PDF files, extracts text, combines it with text from another PDF obtained from an Express app, interacts with the Gemini API to extract workflow data from the combined text, processes the extracted data, and returns the extracted workflow data.

## Setup

### Installation

Install the required dependencies using pip:

```bash
pip install Flask flask_cors PyPDF2 requests
````

### Running the Flask App

Execute the following command to run the Flask application:

```bash
python app.py
```

## Endpoints

### 1. Facturisation Endpoint

- **URL:** `/facturisation`
- **Method:** POST, OPTIONS
- **Description:**
  - Accepts PDF files for facturisation.
  - Extracts text from the PDF.
  - Interacts with an Express app to obtain modal data.
  - Generates a bill text based on the modal data.
- **Request Parameters:**
  - `file`: PDF file (multipart/form-data)
- **Response:**
  - JSON object containing the generated bill text.

### 2. Workflow Extraction Endpoint

- **URL:** `/extract_key_elements`
- **Method:** POST, OPTIONS
- **Description:**
  - Accepts PDF files for extracting key workflow elements.
  - Extracts text from the PDF and another PDF obtained from an Express app.
  - Interacts with the Gemini API to extract workflow data from the combined text.
  - Processes the extracted workflow data.
- **Request Parameters:**
  - `file`: PDF file (multipart/form-data)
- **Response:**
  - JSON object containing the extracted workflow data.

## Usage

1. Ensure the Flask app is running.
2. Send a POST request to the appropriate endpoint with a PDF file attached.
3. Receive the generated bill text or extracted workflow data in the response.

## Dependencies

- **Flask:** A micro web framework for Python.
- **flask_cors:** A Flask extension for handling Cross-Origin Resource Sharing (CORS).
- **PyPDF2:** A library for reading and manipulating PDF files.
- **requests:** A library for making HTTP requests.

## Credits

- This application was created by [Your Name].

```

```
