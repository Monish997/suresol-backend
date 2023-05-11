from datetime import datetime

from flask import Blueprint
from fuzzywuzzy.process import extract

from suresol.chat.forms import ChatForm

chat = Blueprint('chat', __name__)

map = {
    "hey": "Hello! How can I help you?",
    "hello": "Hello! How can I help you?",
    "i'm not feeling well": "I'm sorry to hear that. Can you tell me more about it?",
    "i'm depressed": "I'm sorry to hear that. Can you tell me more about it?",
    "i'm feeling suicidal": "I'm sorry to hear that. Suicide is never the answer! Please seek professional help immediately.",
    "i'm having suicidal thoughts": "I'm sorry to hear that. Suicide is never the answer! Please seek professional help immediately.",
    "i don't feel safe": "Use the SOS button to trigger an alert to your emergency contacts.",
    "i need help": "Use the SOS button to trigger an alert to your emergency contacts.",
    "i'm feeling unsafe": "Use the SOS button to trigger an alert to your emergency contacts.",
    "i'm not feeling safe": "Use the SOS button to trigger an alert to your emergency contacts.",
}
choices, responses = zip(*map.items())

@chat.route('/chat', methods=['POST'])
def chat_reply():
    form = ChatForm()
    if form.validate_on_submit():
        matches = extract(form.message.data, choices, limit=3)
        print(datetime.now().strftime("%c"), form.message.data, matches)
        if not matches:
            return {"message": "I'm sorry, I didn't understand that."}, 200
        idx = choices.index(matches[0][0])
        return {"message": responses[idx]}, 200
    return {"error": "Bad Request"}, 400
