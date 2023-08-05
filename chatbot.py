import os
import logging
import gradio as gr
from fitness_agent import FitnessAgent
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load environment variables from .env.list
load_dotenv('.env.list')

# Now you can access the variables using os.environ
openai_api_key = os.getenv('OPENAI_API_KEY')
nut_api_key = os.getenv('NUT_API_KEY')

# Instantiate FitnessAgent here so it remains open
fitness_agent = FitnessAgent(openai_api_key, nut_api_key)

def get_response(message, history):

    logger.info(f'Chat history: {history}')

    formatted_chat_history = [
        {
            'role': 'system',
            'content': 'Assistant is a large language model trained by OpenAI.\n\nAssistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussion on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.\n\nAssistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.\n\nOverall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.\n'
        }
    ]

    if history:
        for i, chat in enumerate(history[0]):
            formatted_chat_history.append({
                'role': 'user' if i % 2 == 0 else 'assistant',
                'content': chat
            })

        logger.info(formatted_chat_history)
        fitness_agent.chat_history = formatted_chat_history

        logger.info(fitness_agent.chat_history)

    # Get raw chat response
    res = fitness_agent.ask(message)

    chat_response = res['choices'][0]['message']['content']

    return chat_response

def main():

    chat_interface = gr.ChatInterface(
        fn=get_response,
        title="Fitness Agent",
        description="A simple chatbot using a Fitness Agent and Gradio with conversation history",
    )

    chat_interface.launch()

if __name__ == "__main__":
    main()