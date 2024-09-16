from flask import Flask, render_template, request, jsonify
from chat import chatbot_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    bot_response = chatbot_response(user_input)
    return jsonify(response=bot_response)

if __name__ == "__main__":
    app.run(debug=False)
