import chainlit as cl

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_history = []
current_temperature = 0.7

@cl.on_chat_start
async def start():
    global chat_history
    chat_history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    welcome = (
        "![Logo](/public/Logo.png)\n\n"
        "Assalam o Allaikum!\n" 
        "👋 i am created by Sami, How may i assist you honey!"
        
    )
    await cl.Message(content=welcome).send()

@cl.on_settings_update
async def update_settings(settings):
    global current_temperature
    current_temperature = settings["temperature"]

@cl.on_message
async def main(message: cl.Message):
    global chat_history

    chat_history.append({"role": "user", "content": message.content})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=chat_history,
        temperature=current_temperature
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    await cl.Message(content=reply).send()


