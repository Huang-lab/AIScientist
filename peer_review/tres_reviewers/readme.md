# Très Reviewers: Manuscript Review and Improving Assistant

## Introduction

The Manuscript Review Assistant isdesigned to automate the initial review and improvement of manuscripts using the OpenAI GPT API. It processes manuscripts in PDF or DOCX format, extracts text content and generates a review report by querying the GPT API.

Key Insight: Rather provide a singular review from one point of view, Tres Reviewers identify three reviewers of different expertise areas, like human-centric peer-review process, can provide more specific expert insights that can better judge and help improve the manuscript.

## Requirements

- Python 3.6+
- PyPDF2
- python-docx
- python-dotenv
- OpenAI Python SDK

## Installation

1. Ensure Python 3.6 or higher is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. Clone this repository or download the source code to your local machine.

3. Install the required Python packages using pip:

   ```bash
   pip install PyPDF2 python-docx python-dotenv openai
   ```

## Configuration

1. Obtain an API key from [OpenAI](https://openai.com/).

2. Create a `.env` file in the root directory of the project and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Place your manuscript files (PDF or DOCX) in a convenient directory.

2. Run the Manuscript Review Assistant from the terminal. When prompted, enter the full path to the manuscript file you wish to review (replace the example file):

   ```bash
   python python3 tres_reviewers.py

   Enter the path of the manuscript (PDF or DOCX): example/2024.02.02.24302228v1.full.pdf
   ```

3. The tool will process the manuscript, query the GPT API for a review, and generate a review report in the same directory as the manuscript file, named `Tres_review_report_<timestamp>_<original_filename>.txt`.

## Additional Notes

1. The example folder also contains three output where the total read token lengths was adjusted 6-7.5k, where the output goes from the longest (most tokens left) to shortest. Testing was mainly via price-efficient GPT 3.5 turbo (end 2023, beginning 2024), likely GPT 4 models can yield better results.

2. I've also tried other methods, i.e., using multi-agent framework (autogen) to spin one Editor and three reviewers. However it is challenging to get them only to speak up at the time of asking and thus many not required back-and-forth waste the GPT query. Also even when using the same GPT model autogen agents already seem to have quite some token lengths occupied and outputs are typically shorter.

3. Some ideas for future directions: Incorporate other open-source LLMs. Directly improve the Manuscript. Review peer-review to retain only high-quality comments worth addressing.
