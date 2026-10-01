import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# המפתח נקרא ישירות מתוך משתני הסביבה של השרת בצורה מאובטחת
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/', methods=['POST'])
def google_chat_bot():
    event = request.json
    
    user_message = ""
    if event:
        if 'message' in event and 'text' in event['message']:
            user_message = event['message']['text']
        elif 'text' in event:
            user_message = event['text']
        elif 'commonEventObject' in event and 'parameters' in event['commonEventObject']:
            user_message = event['commonEventObject']['parameters'].get('text', '')
            
    if not user_message:
        user_message = "שלום!"

    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }
    
    ai_response_text = "מצטער, אירעה שגיאה בעיבוד התשובה מ-Gemini."
    
    try:
        response = requests.post(GEMINI_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            try:
                ai_response_text = data['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError):
                pass
    except Exception as e:
        ai_response_text = f"שגיאה: {str(e)}"
        
    response_data = {
        "cardsV2": [
            {
                "cardId": "gemini_response_card",
                "card": {
                    "header": {
                        "title": "תשובה מ-Gemini"
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": ai_response_text
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=8080)
