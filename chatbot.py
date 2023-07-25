import gradio as gr
import os
import openai

import logging

from functools import partial
from fitness_agent import FitnessAgent
from langchain.schema import (
    HumanMessage
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def set_openai_api_key(api_key):
    openai.api_key = api_key
    os.environ["OPENAI_API_KEY"] = api_key
    return "OpenAI API Key set successfully."

def set_nut_api_key(api_key):
    os.environ["NUT_API_KEY"] = api_key
    return "Nutrition API Key set successfully."

def get_response(openai_api_key, nut_api_key, user_input, action=None):
    set_openai_api_key(openai_api_key)
    set_nut_api_key(nut_api_key)

    fitness_agent = FitnessAgent(openai_api_key, nut_api_key)

    # Get raw chat response
    fitness_agent.ask(user_input)

    memory = fitness_agent.agent.chat_history

    # Iterate through messages in ChatMessageHistory and format the output
    updated_conversation = '<div style="background-color: hsl(30, 100%, 30%); color: white; padding: 5px; margin-bottom: 10px; text-align: center; font-size: 1.5em;">Chat History</div>'
    logger.info(memory)
    for i, message in enumerate(memory):
        if i != 0:
            if isinstance(message, HumanMessage):
                prefix = "User: "
                background_color = "hsl(0, 0%, 40%)"  # Dark grey background
                text_color = "hsl(0, 0%, 100%)"  # White text
            else:
                prefix = "Chatbot: "
                background_color = "hsl(0, 0%, 95%)"  # White background
                text_color = "hsl(0, 0%, 0%)"  # Black text
            updated_conversation += f'<div style="color: {text_color}; background-color: {background_color}; margin: 5px; padding: 5px;">{prefix}{message["content"]}</div>'
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