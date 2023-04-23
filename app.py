from flask import Flask, render_template, request
from markupsafe import Markup
import openai
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite

openai.api_key = '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'
from flask_ngrok import run_with_ngrok
from flask import Flask
app = Flask(__name__)
run_with_ngrok(app)   # 将flask app对象传递给run_with_ngrok函数
messages = []
@app.route('/')
def home():

    return render_template('index4.html')

@app.route('/get_response', methods=['POST'])

def get_bot_response():
    user_input = request.form['user_input']
    # print(user_input)
    messages.append({'role': 'user', 'content': user_input})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ai_response = completion.choices[0].message['content']
    # print(ai_response)
    messages.append({'role': 'assistant', 'content': ai_response})
    print(messages)
    return  Markup(markdown.markdown(ai_response, extensions=['fenced_code', 'codehilite']))
@app.route('/reset')
def reset():
    global messages
    messages = []
    return "Conversation history has been reset."
if __name__ == '__main__':
    app.run(debug=True)
