import pdfplumber  # type: ignore
import torch  # type: ignore
from transformers import T5Tokenizer, T5ForConditionalGeneration  # type: ignore
import nltk  # type: ignore
from chromadb import Client  # Correct import for ChromaDB Client
from nltk.corpus import stopwords  # type: ignore
import os
import re

# Ensure NLTK resources are available
try:
    nltk.data.path.append('/Users/macbook/nltk_data')  # Set custom NLTK path
    nltk.download('punkt', download_dir='/Users/macbook/nltk_data')
    nltk.download('stopwords', download_dir='/Users/macbook/nltk_data')
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

# Enhanced function to extract citations from the text
def extract_citations(text, page_number):
    citation_patterns = [
        r'\((\w+,\s*\d{4})\)',  # Matches (Author, 2020)
        r'\[\d+\]',             # Matches [1], [2]
        r'(\w+\s\(\d{4}\))',    # Matches Author (2020)
    ]

    citations = []
    for pattern in citation_patterns:
        matches = re.findall(pattern, text)
        lines = text.split('\n')
        for match in matches:
            for line_number, line in enumerate(lines):
                if match in line:
                    citations.append(f"{match} (p. {page_number}, l. {line_number + 1})")
                    break
    return citations

# Function to extract text and citations from a PDF
def extract_text_and_citations_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        citations = []
        for page_number, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                all_text += page_text
                citations += extract_citations(page_text, page_number + 1)
    return all_text, citations

# Create T5 model and tokenizer
def create_t5_model():
    print("Loading T5 model...")
    model = T5ForConditionalGeneration.from_pretrained('t5-large')
    tokenizer = T5Tokenizer.from_pretrained('t5-large')
    return tokenizer, model

# Summarize text using the T5 model
def summarize_text(tokenizer, model, context):
    input_text = f"summarize: {context}"
    inputs = tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=512)

    summary_ids = model.generate(
        inputs, max_length=150, min_length=30, num_beams=4, length_penalty=2.0, early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Suggest questions from summary
def suggest_questions_from_summary(summary):
    words = nltk.word_tokenize(summary.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and word not in stop_words]

    questions = []
    if len(words) > 0:
        questions.append(f"What is the main idea of {words[0]}?")
    if len(words) > 1:
        questions.append(f"How does {words[1]} relate to the overall topic?")
    if len(words) > 2:
        questions.append(f"Why is {words[2]} important?")
    if len(words) > 3:
        questions.append(f"Can you explain the significance of {words[3]}?")
    if len(words) > 4:
        questions.append(f"What are the implications of {words[4]} in this context?")
    
    return questions

# Answer a query based on the PDF context
def answer_query(tokenizer, model, context, question, citations):
    input_text = f"question: {question} context: {context}"
    inputs = tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=512)

    outputs = model.generate(inputs, max_length=600, num_beams=4, early_stopping=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if not answer or len(answer.split()) < 3:
        return "No answer found"

    citation_str = " ".join(citations) if citations else "No citations found."
    return f"Answer: {answer}\nCitations: {citation_str}"

# Initialize ChromaDB client
def initialize_chromadb():
    return Client()

# Add text to ChromaDB
def add_text_to_chromadb(client, text, summary):
    collection = client.create_collection("pdf_documents")
    collection.add(documents=[text], metadatas=[{"summary": summary}], ids=["doc_1"])

# Main function
def main():
    pdf_path = r"/Users/macbook/Desktop/IPQS/backend/anml.pdf"

    try:
        context, citations = extract_text_and_citations_from_pdf(pdf_path)
    except FileNotFoundError as e:
        print(e)
        return

    tokenizer, model = create_t5_model()
    summary = summarize_text(tokenizer, model, context)
    print("\nSummary of the document:")
    print(summary)

    questions = suggest_questions_from_summary(summary)
    print("\nSuggested questions:")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question}")

    client = initialize_chromadb()
    add_text_to_chromadb(client, context, summary)

    print("\nExtracted citations:")
    for citation in citations:
        print(citation)

    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("Exiting the program.")
            break

        answer = answer_query(tokenizer, model, context, query, citations)
        print(answer)

if __name__ == "__main__":
    main()





