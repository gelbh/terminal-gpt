import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import subprocess

# Load environment variables
load_dotenv()

# Main menu options
menu = [
    "Chat with GPT",
    "Execute git commands with GPT",
    "Generate an image with DALL-E",
    "Generate speech with TTS",
    "Exit"
]

# Models
models = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-4",
    "gpt-4-32k"
]

# Voices
voices = [
    "alloy",
    "echo",
    "fable",
    "onyx",
    "nova",
    "shimmer"
]


def colored(*args):
    """Applies ANSI color/style codes to multiple text segments, with validation checks."""
    colors = {
        "": "",
        "black": "\033[0;30m",
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "yellow": "\033[0;33m",
        "blue": "\033[0;34m",
        "purple": "\033[0;35m",
        "cyan": "\033[0;36m",
        "white": "\033[0;37m",
    }
    styles = {
        "": "",
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "underlined": "\033[4m",
        "blink": "\033[5m",
        "reverse": "\033[7m",
        "hidden": "\033[8m"
    }

    colored_text = ""
    for arg in args:
        text = arg[0]
        color = arg[1] if len(arg) > 1 else ""
        style = arg[2] if len(arg) > 2 else ""

        if color not in colors:
            raise ValueError(f"Color '{color}' not recognized.")
        if style not in styles:
            raise ValueError(f"Style '{style}' not recognized.")

        colored_text += f"{styles[style]}{colors[color]}{text}{styles['reset']}"

    return colored_text


def cprint(*args):
    """Prints multiple text segments in specified colors and/or styles."""
    print(colored(*args))
    
    
def cinput(prompt_args):
    """Get input with a prompt displayed in the specified color and/or style."""
    return input(colored(prompt_args)).strip()


def get_choice_from_list(list):
    """
    This function displays a menu and repeatedly asks for the user's choice until a valid option is selected.
    """
    while True:
        cprint(("\nSelect an option:", "blue"))
        for i, selection in enumerate(list, start=1):
            cprint((f"{i}. {selection}", "yellow"))

        choice = cinput(("\nEnter your choice: ", "purple"))

        if choice.isdigit() and 1 <= int(choice) <= len(list):
            return list[int(choice) - 1]
        else:
            cprint(("Invalid choice. Please try again.", "red"))
            

def make_file_in_dir(directory, filename):
    """
    This function creates a file in the specified directory.
    """
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory)
            
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    return os.path.join(directory, filename)
    
    
def save_history_to_file(history):
    """
    This function saves the chat history to a file.
    """
    if not history:
        cprint(("No history to save.", "red"))
        return
    
    file_path = make_file_in_dir("chat_histories", datetime.now().strftime("%Y%m%d_%H%M%S.json"))

    with open(file_path, 'w') as file:
        json.dump(history, file, indent=4)
        
    cprint((f"History saved to {file_path}", "green"))
    

def color_parts_of_string(string, regex, part_color, string_color):
    if regex in string:
        parts = string.split(regex)
        formatted_string = ""
        is_part = False
        for part in parts:
            if is_part:
                formatted_string += colored((part, part_color))
            else:
                formatted_string += colored((part, string_color))
            is_part = not is_part
        return formatted_string
    else:
        return string

def chat_with_gpt(client, prompt, model, history):
    """
    This function takes a natural language prompt and uses GPT to generate a response.
    """
    try:
        messages = history + [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        
        response = response.choices[0].message.content
        
        return colored((response, "green"))
    except Exception as e:
        return colored((f"An unexpected error occurred: {e}", "red"))
    
    
def generate_image_with_dall_e(client, prompt):
    """
    This function takes a natural language prompt and uses DALL-E to generate an image.
    """
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        return colored((response.data[0].url, "green"))
    except Exception as e:
        return colored((f"An unexpected error occurred: {e}", "red"))
    
    
def generate_speech_with_tts(client, prompt):
    """
    This function takes a natural language prompt and uses TTS to generate speech.
    """
    try:
        voice = get_choice_from_list(voices)
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=prompt
        )
        
        file_path = make_file_in_dir("speeches", datetime.now().strftime("%Y%m%d_%H%M%S.mp3"))
        response.stream_to_file(file_path)
        
        return colored((f"Audio saved to {file_path}", "green"))
    except Exception as e:
        return colored((f"An unexpected error occurred: {e}", "red"))
    
    
def execute_git_commands(git_commands):
    """
    This function executes a list of Git commands in the current directory.
    """
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        for cmd in git_commands:
            cprint(("Executing: ", ""), (cmd, "blue"))
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True)
            cprint((result.stdout.decode(), "green"))
    except subprocess.CalledProcessError as e:
        cprint(("Error executing git command:: ", ""), (e.output.decode(), "red"))


def extract_git_commands_from_text(text):
    """
    This function extracts git commands from a string.
    """
    def is_valid_git_command(command):
        if command.startswith(("`git", "git")):
            return True
        return False

    git_commands = text.strip().split('\n')
    return [cmd.strip() for cmd in git_commands if cmd.strip() and is_valid_git_command(cmd)]


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("The OPENAI_API_KEY environment variable is not set")
    
    client = OpenAI(api_key=api_key)
    if not client:
        raise ValueError("Could not initialize the OpenAI client")
    
    history = []
    
    try:
        while True:
            menu_choice = get_choice_from_list(menu)
            
            if menu_choice == menu[3]:
                return
            elif menu_choice in [menu[0], menu[1]]:    
                model = get_choice_from_list(models)
            
            while True:
                prompt = cinput(("\nYou: ", "purple"))
                
                if prompt.lower() in ["exit", "quit", "q"]:
                    if not history:
                        return
                    
                    save_confirmation = cinput(("\nDo you want to save the chat history before exiting? (y/n): ", "blue")).lower()
                    if save_confirmation == 'y':
                        save_history_to_file(history)
                        
                    break
                elif not prompt:
                    cprint(("\nPlease enter a prompt", "red"))
                    continue
                
                if menu_choice == menu[0]:
                    response = chat_with_gpt(client, prompt, model, history)
                    response = color_parts_of_string(response, "```", "blue", "green")
                    response = color_parts_of_string(response, "`", "blue", "green")
                    cprint(("\nGPT: ", "purple"), (response, ""))
                elif menu_choice == menu[1]:
                    prompt = f"Translate this into a series of git commands: {prompt}"
                    response = chat_with_gpt(client, prompt, model, history)
                    
                    git_commands = extract_git_commands_from_text(response)
                    if git_commands:
                        cprint(("\nSuggested git commands:", "yellow"))
                        for cmd in git_commands:
                            cprint((cmd, "cyan"))
                            
                    options = [
                        "Execute git commands",
                        "Ask to fix",
                        "Exit"
                    ]
                    option = get_choice_from_list(options)
                    if option == options[0]:
                        execute_git_commands(git_commands)
                        return
                    elif option == options[1]:
                        continue
                    else:
                        return
                elif menu_choice == menu[2]:
                    response = generate_image_with_dall_e(client, prompt)
                    cprint(("\nDALL-E: ", "purple"), (response, ""))
                elif menu_choice == menu[3]:
                    response = generate_speech_with_tts(client, prompt)
                    cprint(("\nTTS: ", "purple"), (response, ""))

                history.append({"role": "user", "content": prompt})
                history.append({"role": "system", "content": response})
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
