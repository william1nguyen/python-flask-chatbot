from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_diablo_response(input)


def get_openai_response(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    completions_model = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "Acting like you are megumin-chan in konosuba."},
        {"role":"user", "content":"You are megumin-chan in konosuba" + prompt}
    ]
    response = openai.ChatCompletion.create(
        model=completions_model,
        messages=messages
    )['choices'][0]['message']['content']
    return response

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def get_diablo_response(prompt):
    for step in range(5):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(str(prompt) + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

if __name__ == '__main__':
    app.run()