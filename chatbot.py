import gradio as gr
import os
import openai

import logging
import threading

from functools import partial
from fitness_agent import FitnessAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def set_openai_api_key(api_key):
    openai.api_key = api_key
    os.environ["OPENAI_API_KEY"] = api_key
    return "OpenAI API Key set successfully."

def set_nut_api_key(api_key):
    os.environ["NUT_API_KEY"] = api_key
    return "Nutrition API Key set successfully."

# Initialize the global fitness_agent
fitness_agent = None

# Initialize a lock for the fitness_agent
fitness_agent_lock = threading.Lock()

def get_response(openai_api_key, nut_api_key, user_input, action=None):
    global fitness_agent
    set_openai_api_key(openai_api_key)
    set_nut_api_key(nut_api_key)

    with fitness_agent_lock:
        if fitness_agent is None:
            # Initialize the fitness agent if it is None
            fitness_agent = FitnessAgent(openai_api_key, nut_api_key)

    # Get raw chat response
    fitness_agent.ask(user_input)

    memory = fitness_agent.agent.chat_history

    # Iterate through messages in ChatMessageHistory and format the output
    updated_conversation = '<div style="background-color: hsl(30, 100%, 30%); color: white; padding: 5px; margin-bottom: 10px; text-align: center; font-size: 1.5em;">Chat History</div>'
    logger.info(memory)
    for i, message in enumerate(memory):
        if i != 0:
            if message['role'] == 'user':
                prefix = "User: "
                background_color = "#D3D3D3"  # Light grey background
                text_color = "#000000"  # Black text
            else:
                prefix = "Chatbot: "
                background_color = "#F0F8FF"  # Alice blue background
                text_color = "#000000"  # Black text

            formatted_message = message["content"].replace('\n', '<br>')
            
            updated_conversation += f'<div style="color: {text_color}; background-color: {background_color}; margin: 5px; padding: 5px;">{prefix}<br>{formatted_message}</div>'
    return updated_conversation

def main():

    openai_api_key = gr.components.Textbox(
        lines=1,
        label="Enter OpenAI API Key",
        type="password",
    )

    nut_api_key = gr.components.Textbox(
        lines=1,
        label="Enter Nutrition API Key",
        type="password",
    )

    question = gr.components.Textbox(
        lines=3,
        label="Enter your message",
    )

    output_history = gr.outputs.HTML(
        label="Updated Conversation",
    )

    inputs = [
        openai_api_key,
        nut_api_key,
        question,
    ]

    iface = gr.Interface(
        fn=partial(get_response),
        inputs=inputs,
        outputs=[output_history],
        title="Fitness Agent",
        description="A simple chatbot using a Fitness Agent and Gradio with conversation history",
        allow_flagging=False,
    )

    iface.launch()

if __name__ == "__main__":
    main()
