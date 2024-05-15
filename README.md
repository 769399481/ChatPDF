# PDF-Quick-Reader

PDF Quick Reader is a simple application built on Flask and Elasticsearch for quickly reading and searching PDF documents and providing Q&A functionality. The application uploads PDF files and extracts the text from them, storing it in Elasticsearch for full-text search. Users can perform text searches in the uploaded PDF files and get relevant Q&A information.

## Functional characteristics

- Upload PDF files: Users can upload their own PDF files for text extraction and search.
- Text Extraction: The application will automatically extract the text content from the uploaded PDF file and store it in Elasticsearch.
- Text Search: Users can search the text in the uploaded PDF files by entering query terms.
- Q&A Function: The application searches for relevant information in the text content based on the query words provided by the user and uses the GPT model to generate relevant Q&A information.
