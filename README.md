# PDF-Quick-Reader

PDF Quick Reader is a simple application built on Flask and Elasticsearch for quickly reading and searching PDF documents and providing Q&A functionality. The application uploads PDF files and extracts the text from them, storing it in Elasticsearch for full-text search. Users can perform text searches in the uploaded PDF files and get relevant Q&A information.

## Functional characteristics

- Upload PDF files: Users can upload their own PDF files for text extraction and search.
- Text Extraction: The application will automatically extract the text content from the uploaded PDF file and store it in Elasticsearch.
- Text Search: Users can search the text in the uploaded PDF files by entering query terms.
- Q&A Function: The application searches for relevant information in the text content based on the query words provided by the user and uses the GPT model to generate relevant Q&A information.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/769399481/PDF-Quick-Reader.git
   ```
2. Install dependencies using conda:
   ```
   conda create --name pdf-reader-env --file requirements.txt
   ```
3. Activate the conda environment:
   ```
   conda activate pdf-reader-env
   ```
4. Set up Elasticsearch:
   If you provide the Elasticsearch server's address, port, and username and password for accessing it, you do not need to manually download the Elasticsearch server. the Elasticsearch client for Python   automatically establishes a connection to the remote Elasticsearch server.
   ```
   es = Elasticsearch(
     hosts=['x'],  # service address and port
     http_auth=("xx", "xxxx"),  # User name, password
   )
   index_name = "xxxx" # Defining Index Names
   ```
5. Set up OpenAI:
   - Sign up for an API key on the [DevAGI website](https://devcto.com/).
   - Create a .env file in the project directory and add your OPENAI_API_KEY and OPENAI_BASE_URL:
   ```
   OPENAI_API_KEY="xxxxxx"
   OPENAI_BASE_URL="xxxxxx"
   ```
6. Run the Flask application:
   ```
   python app.py
   ```

## Usage

1. Access the application in your web browser.
2. Upload a PDF file using the provided interface(Images and tables are currently not supported).
3. Ask questions related to the content of the uploaded PDF.
4. View the answers provided by the system.

## Contributor

- Hao

## License

This project is licensed under the MIT License - see the LICENSE file for details.
