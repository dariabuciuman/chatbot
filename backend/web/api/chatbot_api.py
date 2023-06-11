import json
import os
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from helpers.text_processing import remove_diacritics
from web.chatbot_entity import LegalChatbot

app = Flask(__name__)

chatbot_global = None
CORS(app, origins='*')


def load_chatbot():
    global chatbot_global
    classes_dir = '../../neural/classes.pkl'
    intents_dir = '../../helpers/good_intents.json'
    model_dir = '../../neural/keywords_model.h5'
    words_dir = '../../neural/words.pkl'
    chatbot_global = LegalChatbot(classes_dir=classes_dir, words_dir=words_dir, intents_dir=intents_dir,
                                  model_dir=model_dir)


@app.route("/api/chatbot/response", methods=['POST'])
def get_response_for_message():
    data = request.get_json()
    message = data.get("message")
    print("Received message %s", message)
    global chatbot_global
    if chatbot_global is None:
        load_chatbot()
    chatbot_global.start_chatbot()
    response = chatbot_global.get_response_for_message(message)
    print("Report saved")
    return jsonify({"response": response})


@app.route('/api/chatbot/report', methods=['POST'])
def save_report():
    if not os.path.exists('bugs'):
        os.makedirs('bugs')

    report_data = request.get_json()
    message = report_data.get('chat')

    # Generate the report name with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_name = f"report_{timestamp}.json"

    # Save the message to a JSON file
    file_path = os.path.join('bugs', report_name)
    with open(file_path, 'w') as file:
        json.dump(message, file)

    return "Report saved successfully"


if __name__ == '__main__':
    app.run()
