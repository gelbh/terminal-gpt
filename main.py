import json
import os
from openai import OpenAI, RateLimitError, OpenAIError
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Define color codes for terminal output
colors = {
    "black": "\033[0;30m",
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[0;33m",
    "blue": "\033[0;34m",
    "purple": "\033[0;35m",
    "cyan": "\033[0;36m",
    "white": "\033[0;37m",
    "bold_black": "\033[1;30m",
    "bold_red": "\033[1;31m",
    "bold_green": "\033[1;32m",
    "bold_yellow": "\033[1;33m",
    "bold_blue": "\033[1;34m",
    "bold_purple": "\033[1;35m",
    "bold_cyan": "\033[1;36m",
    "bold_white": "\033[1;37m",
    "reset": "\033[0m"
}

# Get the API key from environment variables
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Function to chat with a specified GPT model
def chat_with_gpt(prompt, history, model):
    try:
        messages = history + [{"role": "user", "content": prompt}]
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return completion.choices[0].message.content
    except RateLimitError:
        return "Rate limit exceeded. Please try again later."
    except OpenAIError as e:
        return f"An error occurred with the OpenAI service: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    
# Function to save chat history to a file
def save_history_to_file(history):
    # Check if history is empty
    if not history:
        print(f"{colors['red']}\n\nNo history to save.{colors['reset']}")
        return
    
    # Ensure the folder exists
    if not os.path.exists("chat_histories"):
        os.makedirs("chat_histories")
        
    # Create a timestamped filename
    filename = datetime.now().strftime("%Y%m%d_%H%M%S.json")
    file_path = os.path.join("chat_histories", filename)

    # Write the history to the file
    with open(file_path, 'w') as file:
        json.dump(history, file, indent=4)
        
    print(f"{colors['green']}\n\nHistory saved to {file_path}{colors['reset']}")
    
# Main function to run the script
def main():
    history = []
    
    # Ask user to select a model
    print(f"{colors['blue']}Select a GPT model:{colors['reset']}")
    print(f"{colors['yellow']}1. GPT-3.5 Turbo{colors['reset']}")
    print(f"{colors['yellow']}4. Other model (please specify){colors['reset']}")
    model_choice = input(f"{colors['purple']}\nEnter your choice: {colors['reset']}").strip()
    
    # Set the model based on user input
    if model_choice == "1":
        model = "gpt-3.5-turbo"
    elif model_choice == "2":
        model = input(f"{colors['purple']}Enter model name: {colors['reset']}").strip()
        if not model:
            model = "gpt-3.5-turbo"
    
    try:
        # Chat loop
        while True:
            prompt = input(f"\n{colors["purple"]}You: {colors['reset']}").strip()
            
            # Check for special commands
            if prompt.lower() in ["exit", "quit"]:
                save_confirmation = input(f"{colors['blue']}\nDo you want to save the chat history before exiting? (y/n): {colors['reset']}").strip().lower()
                if save_confirmation == 'y':
                    save_history_to_file(history)
                break
            elif not prompt:
                print(f"{colors["red"]}Please enter a prompt{colors["reset"]}")
                continue
            
            response = chat_with_gpt(prompt, history, model)
            history.append({"role": "user", "content": prompt})
            history.append({"role": "system", "content": response})
            
            print("\n" + colors["purple"] + "GPT:" + colors["green"], response, colors["reset"])
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
