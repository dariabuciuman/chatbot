import json
import os
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from web.chatbot_entity import LegalChatbot

app = Flask(__name__)

CORS(app, origins='*')


def load_chatbot():
    classes_dir = '../../neural/classes.pkl'
    intents_dir = '../../helpers/good_intents_original.json'
    model_dir = '../../neural/keywords_model3.h5'
    words_dir = '../../neural/words.pkl'
    chatbot = LegalChatbot(classes_dir=classes_dir, words_dir=words_dir, intents_dir=intents_dir,
                           model_dir=model_dir)
    return chatbot


@app.route("/api/chatbot/response", methods=['POST'])
def get_response_for_message():
    data = request.get_json()
    message = data.get("message")
    print("Received message %s", message)
    chatbot = load_chatbot()
    chatbot.start_chatbot()
    response = chatbot.get_response_for_message(message)
    return jsonify({"response": response})


@app.route('/api/chatbot/report', methods=['POST'])
def save_report():
    if not os.path.exists('bugs'):
        os.makedirs('bugs')

    report_data = request.get_json()
    message = report_data.get('chat')
    print(message)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_name = f"report_{timestamp}.json"

    file_path = os.path.join('bugs', report_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(message, file, ensure_ascii=False)

    return "Report saved successfully"


if __name__ == '__main__':
    app.run()
