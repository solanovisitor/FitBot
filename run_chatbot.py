import hupper
import chatbot
from dotenv import load_dotenv, find_dotenv

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    reloader = hupper.start_reloader('chatbot.main')  # Replace 'chatbot.main' with the function that launches your Fitness Agent Gradio app
    chatbot.main()
