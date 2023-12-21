# Python Chatbot with OpenAI

## Overview

This repository contains a Python script for a chatbot that interacts with OpenAI's GPT-3.5 Turbo model. The script features a colorful command-line interface (CLI) for an enhanced user experience. The chatbot maintains a conversation history, allowing for context-aware interactions.

## Prerequisites

- Python 3.x
- `openai` Python package
- `python-dotenv` package for environment variable management

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/gelbh/terminal-gpt.git
   cd terminal=gpt
   ```

2. **Set Up a Virtual Environment (Optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **OpenAI API Key**: You need an API key from OpenAI. You can obtain it from [OpenAI API](https://beta.openai.com/signup/).

2. **Create a `.env` File**:
    - In the root of the project directory, create a file named `.env`.
    - Add your OpenAI API key in this format:
  
      ```makefile
      OPENAI_API_KEY=YOUR-KEY-HERE
      ```

       - Replace **`YOUR-KEY-HERE`** with your actual API key.

## Usage
Run the script with the following command:
```bash
python main.py
```

Enter your prompts in the CLI, and the script will interact with you using OpenAI's GPT model. Type `exit` or `quit` to end the session.

## Notes
- The script uses ANSI color codes for CLI coloring, which might not work correctly on all terminals.
- Keep your API keys secure and never share them in public repositories.
