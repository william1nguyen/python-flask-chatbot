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
    return get_openai_response(input)


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


if __name__ == '__main__':
    app.run()