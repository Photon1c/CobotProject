#Memory management using simple text file for chatbot
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import pprint
import time

# Load environment variables
load_dotenv()
client = OpenAI()

# Initialize chat log
start_chat_log = '''Human: Hello, who are you?
AI: I am an AI assistant. How can I help you today?
'''

# Pretty printer for formatted output
pp = pprint.PrettyPrinter(indent=2)

def save_chat_to_file(chat_log, filename=None):
    """Save the chat log to a text file with timestamp in filename"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.txt"
    
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(chat_log)
        print(f"Chat saved to {filename}")
        return filename
    except Exception as e:
        print(f"Error saving chat: {e}")
        return None

def load_chat_from_file(filename):
    """Load a chat log from a text file"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error loading chat: {e}")
        return start_chat_log

def summarize_conversation(chat_log):
    """Use GPT-4o to summarize the conversation"""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes conversations. Create a concise summary that captures the key points, questions, and information exchanged. The summary should be useful as context for continuing the conversation."},
                {"role": "user", "content": f"Summarize this conversation:\n\n{chat_log}"}
            ]
        )
        summary = completion.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"Error summarizing conversation: {e}")
        return "Failed to summarize conversation."

def create_messages_with_window(chat_log, window_size=5, include_summary=True):
    """Convert chat log to structured messages with windowing and optional summary"""
    # Start with system message
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Add summary of older conversation if available and requested
    if include_summary and len(chat_log.split('\n')) > window_size * 2:
        summary = summarize_conversation(chat_log)
        messages.append({"role": "system", "content": f"Summary of previous conversation: {summary}"})
    
    # Parse recent messages from chat log
    lines = chat_log.strip().split('\n')
    # Only take the most recent exchanges based on window_size
    if len(lines) > window_size * 2:
        lines = lines[-(window_size * 2):]
    
    # Convert to message format
    current_role = None
    current_content = []
    
    for line in lines:
        if line.startswith("Human: "):
            # If we were building an assistant message, add it
            if current_role == "assistant" and current_content:
                messages.append({"role": current_role, "content": "\n".join(current_content)})
                current_content = []
            
            # Start building a user message
            current_role = "user"
            current_content.append(line[7:])  # Remove "Human: " prefix
        
        elif line.startswith("AI: "):
            # If we were building a user message, add it
            if current_role == "user" and current_content:
                messages.append({"role": current_role, "content": "\n".join(current_content)})
                current_content = []
            
            # Start building an assistant message
            current_role = "assistant"
            current_content.append(line[4:])  # Remove "AI: " prefix
        
        else:
            # Continue with current message
            if current_role:
                current_content.append(line)
    
    # Add the last message if any
    if current_role and current_content:
        messages.append({"role": current_role, "content": "\n".join(current_content)})
    
    return messages

def ask(question, chat_log=None):
    """Send a question to the API and get a response with context windowing"""
    if chat_log is None:
        chat_log = start_chat_log
    
    try:
        # Create windowed message context
        messages = create_messages_with_window(chat_log)
        
        # Add the current question
        messages.append({"role": "user", "content": question})
        
        # Debug info about token usage (optional)
        print("Sending messages to API:")
        pp.pprint([(m["role"], len(m["content"].split())) for m in messages])
        
        # Make API call
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        
        answer = completion.choices[0].message.content.strip()
        return answer
    
    except Exception as e:
        print(f"Error in API call: {e}")
        return f"I'm sorry, I encountered an error: {str(e)}"

def append_interaction_to_chat_log(question, answer, chat_log=None):
    """Add the new interaction to the chat log"""
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'

def start_interaction():
    """Main chat loop with file saving functionality and memory management"""
    # Try to load most recent chat or start fresh
    chat_files = [f for f in os.listdir() if f.startswith("chat_history_") and f.endswith(".txt")]
    
    if chat_files:
        most_recent = max(chat_files)
        load_option = input(f"Found previous chat ({most_recent}). Load it? (y/n): ").lower()
        
        if load_option.startswith('y'):
            chat_log = load_chat_from_file(most_recent)
            current_file = most_recent
        else:
            chat_log = start_chat_log
            current_file = None
    else:
        chat_log = start_chat_log
        current_file = None
    
    print("\n" + "="*50)
    print("Chat started. Commands:")
    print("  'quit', 'exit', 'bye' - End conversation")
    print("  'save' - Save conversation")
    print("  'summary' - Get conversation summary")
    print("="*50 + "\n")
    
    # If we have a long chat history, summarize it
    if len(chat_log.split('\n')) > 20:
        print("Summarizing previous conversation...")
        summary = summarize_conversation(chat_log)
        print(f"\nSummary of previous conversation:\n{summary}\n")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        # Handle special commands
        if user_input.lower() in ['quit', 'exit', 'bye']:
            save_option = input("Would you like to save this chat before quitting? (y/n): ").lower()
            if save_option.startswith('y'):
                if current_file:
                    save_option = input(f"Update existing file ({current_file})? (y/n): ").lower()
                    if save_option.startswith('y'):
                        save_chat_to_file(chat_log, current_file)
                    else:
                        save_chat_to_file(chat_log)
                else:
                    save_chat_to_file(chat_log)
            print("Goodbye!")
            break
            
        if user_input.lower() == 'save':
            if current_file:
                save_option = input(f"Update existing file ({current_file})? (y/n): ").lower()
                if save_option.startswith('y'):
                    save_chat_to_file(chat_log, current_file)
                else:
                    current_file = save_chat_to_file(chat_log)
            else:
                current_file = save_chat_to_file(chat_log)
            continue
        
        if user_input.lower() == 'summary':
            print("\nGenerating conversation summary...")
            summary = summarize_conversation(chat_log)
            print(f"\nSummary:\n{summary}")
            continue
            
        # Get AI response with pretty formatting for output
        print("\nThinking...")
        start_time = time.time()
        ai_response = ask(user_input, chat_log)
        end_time = time.time()
        
        print(f"\nAI: {ai_response}")
        print(f"\n[Response time: {end_time - start_time:.2f}s]")
        
        # Update chat log
        chat_log = append_interaction_to_chat_log(user_input, ai_response, chat_log)
        
        # Auto-save every few exchanges
        if chat_log.count("Human:") % 5 == 0:
            if current_file:
                save_chat_to_file(chat_log, current_file)
            else:
                current_file = save_chat_to_file(chat_log)
            print("(Chat auto-saved)")

if __name__ == "__main__":
    start_interaction()
