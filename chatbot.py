import gradio as gr
import os
from functools import partial

from fitness_agent import FitnessAgent

def set_api_key(api_key):
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["NUT_API_KEY"] = api_key
    return "API Key set successfully."

def get_response(fitness_agent, api_key, user_input):
    set_api_key(api_key)

    # Get raw chat response
    response = fitness_agent.ask(user_input)

    # Format the output
    updated_conversation = '<div style="background-color: hsl(30, 100%, 30%); color: white; padding: 5px; margin-bottom: 10px; text-align: center; font-size: 1.5em;">Chat History</div>'
    for i, message in enumerate(fitness_agent.view_chat_history()):
        prefix = "User: " if message['role'] == "user" else "FitnessAgent: "
        background_color = "hsl(0, 0%, 40%)" if message['role'] == "user" else "hsl(0, 0%, 95%)"
        text_color = "hsl(0, 0%, 100%)" if message['role'] == "user" else "hsl(0, 0%, 0%)"
        updated_conversation += f'<div style="color: {text_color}; background-color: {background_color}; margin: 5px; padding: 5px;">{prefix}{message["content"]}</div>'
    return updated_conversation

def main():
    api_key = os.getenv('OPENAI_API_KEY')
    nutrition_api_key = os.getenv('NUT_API_KEY')

    api_key_input = gr.components.Textbox(
        lines=1,
        label="Enter OpenAI API Key",
        value=api_key,
        type="password",
    )

    nutrition_api_key_input = gr.components.Textbox(
        lines=1,
        label="Enter Nutrition API Key",
        value=nutrition_api_key,
        type="password",
    )

    user_input = gr.components.Textbox(
        lines=3,
        label="Enter your message",
    )

    output_history = gr.outputs.HTML(
        label="Updated Conversation",
    )

    fitness_agent = FitnessAgent(api_key, nutrition_api_key)

    inputs = [
        api_key_input,
        nutrition_api_key_input,
        user_input,
    ]

    iface = gr.Interface(
        fn=partial(get_response, fitness_agent),
        inputs=inputs,
        outputs=[output_history],
        title="Fitness Agent",
        description="A simple chatbot using a Fitness Agent and Gradio with conversation history",
        allow_flagging=False,
    )

    iface.launch()

if __name__ == "__main__":
    main()