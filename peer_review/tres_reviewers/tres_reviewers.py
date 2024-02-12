import os
import re
from datetime import datetime

from docx import Document
from dotenv import load_dotenv
import PyPDF2
from openai import OpenAI

# Load the .env file
load_dotenv()
# Get the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def clean_and_truncate_text(text):
    """Cleans text by removing extra spaces and newlines, and truncates at references or acknowledgments."""
    text = ' '.join(text.split())  # Remove extra spaces
    text = re.sub(r'\n+', '\n', text).strip()  # Remove extra newlines
    # Truncate text at references or acknowledgements
    match = re.search(r'(Reference\(s\)(\s+|\n))', text, re.IGNORECASE)
    return text[:match.start()] if match else text


def read_pdf(file_path):
    """Reads text from a PDF file, cleans it, and truncates at references or acknowledgments."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''.join(clean_and_truncate_text(page.extract_text())
                       for page in reader.pages)
    return text


def read_word(file_path):
    """Reads text from a Word document, cleans it, and truncates at references or acknowledgments."""
    doc = Document(file_path)
    text = '\n'.join(clean_and_truncate_text(paragraph.text)
                     for paragraph in doc.paragraphs)
    return text

# Function to interact with GPT API for manuscript peer review


def query_gpt(text, section_name, model="gpt-3.5-turbo-0125"):
    """
    Queries the GPT API to generate comments for a given section of text based on specified instructions.

    Parameters:
    - text (str): The text for which comments are to be generated.
    - section_name (str): The name of the section being reviewed, used for contextualizing the query.

    Returns:
    - str: The generated comments from the GPT API.
    """
    # Clear and concise instructions for the GPT model
    instructions = (
        f"As a helpful, world-class scientist, read the manuscript'\
        to identify three major expertise areas, then assume the role of each of three experts\
        to provide 3 bullet points of the study's key strengths, weaknesses, and suggested improvements.\
        Let's think step by step."
    )

    # Structured prompt for GPT API
    prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": instructions},
        {"role": "assistant", "content": f"Section: {section_name}\n{text}"}
    ]

    # API call to GPT with the constructed prompt
    response = client.chat.completions.create(
        model=model, messages=prompt)

    # Extracting and returning the generated content
    return response.choices[0].message.content

# this is if we split the reviews into different sections, currently not needed as token lengths expanded substaintially
# now we focus on the first 6000k token, sufficient for most well-written manuscripts
# this token limits helps the LLM not run out of token when generating reviews
# if one uses a more powerful model with longer contexts length, could easily expand the # of tokens


def split_into_sections(text, max_tokens=6000):
    """
    Splits the given text into sections, each with a maximum number of tokens.

    Parameters:
    - text (str): The text to be split.
    - max_tokens (int): The maximum number of tokens allowed per section.

    Returns:
    - dict: A dictionary of sections with keys as section names and values as section texts.
    """
    words = text.split()
    sections = {}
    for i in range(0, len(words), max_tokens):
        section_text = " ".join(words[i:i+max_tokens])
        section_name = f"Section {len(sections)+1}: Start...{section_text[:50]}...End {section_text[-50:]}"
        sections[section_name] = section_text
    return sections


def main():
    """
    Main function to process manuscripts. Reads the manuscript, splits it into sections, 
    queries GPT for the first section, and writes the review to a file.
    """
    file_path = input("Enter the path of the manuscript (PDF or DOCX): ")
    if not os.path.exists(file_path):
        print("File path does not exist. Please check the path and try again.")
        return

    file_extension = os.path.splitext(file_path)[1].lower()
    read_function = read_pdf if file_extension == '.pdf' else read_word if file_extension == '.docx' else None

    if not read_function:
        print(
            f"Unsupported file format: {file_extension}. Please use PDF or DOCX files.")
        return

    manuscript_text = read_function(file_path)
    manuscript_sections = split_into_sections(manuscript_text)

    for section_name, section_text in manuscript_sections.items():
        gpt_response = query_gpt(section_text, section_name)
        break  # Process only the first section for now

    # Prepare and write the review report
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    original_filename = os.path.basename(file_path).replace(" ", "_")
    report_filename = f"Tres_review_report_{timestamp}_{original_filename}.txt"

    with open(report_filename, "w") as report_file:
        report_file.write(f"AI Review of {section_name}:\n{gpt_response}\n")

    print(f"Review report saved as: {report_filename}")


if __name__ == '__main__':
    main()
