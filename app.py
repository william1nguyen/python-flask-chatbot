from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
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
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

def get_diablo_response(prompt):
    # Generate a response using the pipeline
    response = generator(prompt, max_length=1000, num_return_sequences=1)[0]['generated_text']

    # Remove special tokens from the response
    response = tokenizer.decode(tokenizer.encode(response, add_special_tokens=False), skip_special_tokens=True)

    return response

if __name__ == '__main__':
    port = 5050
    app.run('0.0.0.0', port)