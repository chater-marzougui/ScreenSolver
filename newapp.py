import os
import json
import PyPDF2
from PyPDF2 import PdfReader
import google.generativeai as genai
import time
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv("API_KEY")
CHUNK_SIZE = 10  # Number of pages per chunk

# Initialize Gemini
genai.configure(api_key=API_KEY)

def split_pdf_into_chunks(pdf_path, chunk_size=CHUNK_SIZE):
    """Split a PDF into chunks of specified size."""
    print(f"Opening PDF: {pdf_path}")
    try:
        pdf = PdfReader(pdf_path)
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")
        
        chunks = []
        for i in range(0, total_pages, chunk_size):
            end_page = min(i + chunk_size, total_pages)
            chunk_text = ""
            
            print(f"Processing pages {i+1} to {end_page}")
            for page_num in range(i, end_page):
                page = pdf.pages[page_num]
                chunk_text += page.extract_text() + "\n\n"
            
            chunks.append({
                "start_page": i + 1,
                "end_page": end_page,
                "text": chunk_text
            })
            
        return chunks
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []

def get_gemini_response(text, attempts=3, delay=5):
    """Get response from Gemini with retry logic."""
    prompt = f"""
Analyze the provided document in detail and extract the key concepts, definitions, and critical points necessary for a deep understanding of the course. Then, generate multiple-choice questions (QCM), following the format below:
Questions should be clear, precise, and relevant to the document's content.
The answer choices (options) should include one correct answer and three plausible distractors.
The correct answer should be indicated with its index in the list.
Provide a brief yet informative explanation for each answer to reinforce understanding.
Ensure the questions cover various levels of cognition, including factual recall, comprehension, and application.
Structure the questions to promote critical thinking and not just rote memorization.
Use the following JSON format:
{{
    "seance 1": [
        {{
            "question": "Quel était le montant approximatif du financement mondial en capital-risque des startups au troisième trimestre 2021 ?",
            "options": [
                "77 milliards USD",
                "158 milliards USD",
                "100 milliards USD",
                "200 milliards USD"
            ],
            "answer": 1,
            "explanation": "Le financement mondial en capital-risque des startups au troisième trimestre 2021 s'élevait à environ 158 milliards USD."
        }},
        {{
            "question": "Combien de nouvelles licornes ont émergé au troisième trimestre 2021 ?",
            "options": [
                "37",
                "77",
                "200",
                "127"
            ],
            "answer": 3,
            "explanation": "Au troisième trimestre 2021, 127 nouvelles licornes ont émergé."
        }}
    ]
}}
Make sure that:
The answers are zero-indexed.
The questions cover different sections of the document comprehensively.
The explanations reinforce key learnings and not just repeat the correct answer.
The difficulty level varies, including both basic and challenging questions.
And be sure to put the answers indexes at different places (Don't repeat the position of correct answer).
Don't put words like "The document says" or "The text states" in the questions nor in the explanation.
The reply should be in JSON format only, without any additional text or comments.
The reply should be in the same language as the document.

Here's the document to analyze:
{text}
"""
    
    model = genai.GenerativeModel('gemini-pro')
    
    for attempt in range(attempts):
        try:
            response = model.generate_content(prompt)
            # Extract the JSON part from the response
            response_text = response.text
            
            # Find the first { and the last } to extract the JSON object
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                # Parse to validate it's proper JSON
                try:
                    json_data = json.loads(json_str)
                    return json_data
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON response (attempt {attempt+1}/{attempts}):\n{json_str}\nError: {e}")
            else:
                print(f"No valid JSON found in response (attempt {attempt+1}/{attempts}):\n{response_text}")
                
        except Exception as e:
            print(f"Error calling Gemini API (attempt {attempt+1}/{attempts}): {e}")
        
        if attempt < attempts - 1:
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            # Increase delay for next retry
            delay *= 2
    
    print("Failed to get a valid response after multiple attempts")
    return {"error": "Failed to get a valid response from Gemini"}

def process_pdf_with_gemini(pdf_path, output_path):
    """Process PDF with Gemini and save results to a JSON file."""
    chunks = split_pdf_into_chunks(pdf_path)
    if not chunks:
        print("No chunks were created. Exiting.")
        return
    
    print(f"Created {len(chunks)} chunks")
    
    all_questions = {}
    
    for i, chunk in enumerate(chunks):
        print(f"\nProcessing chunk {i+1}/{len(chunks)} (pages {chunk['start_page']}-{chunk['end_page']})")
        
        # Get response from Gemini
        print(f"Sending text to Gemini (length: {len(chunk['text'])} characters)")
        response = get_gemini_response(chunk['text'])
        
        if "error" in response:
            print(f"Error in chunk {i+1}: {response['error']}")
            continue
            
        # Merge the response with the combined results
        for section, questions in response.items():
            section_key = f"{section} (p.{chunk['start_page']}-{chunk['end_page']})"
            all_questions[section_key] = questions
            print(f"Added {len(questions)} questions for {section_key}")
        
        # Brief pause between API calls
        if i < len(chunks) - 1:
            time.sleep(2)
    
    # Save the combined results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nComplete! Saved results to {output_path}")
    print(f"Generated a total of {sum(len(q) for q in all_questions.values())} questions")

if __name__ == "__main__":
    # Get input from user
    pdf_path = input("Enter the path to your PDF file: ")
    
    # Generate a default output filename based on the input PDF
    default_output = os.path.splitext(os.path.basename(pdf_path))[0] + "_questions.json"
    output_path = input(f"Enter the output JSON path (default: {default_output}): ").strip()
    if not output_path:
        output_path = default_output
    
    # Process the PDF
    process_pdf_with_gemini(pdf_path, output_path)