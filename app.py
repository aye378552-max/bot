from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# הכנס כאן את מפתח ה-API שיצרת ב-Google AI Studio
AQ.Ab8RN6LiWsz8g5MIp0Eyr_X3tQt3g8ekbCbOk8p98UAQwoVDug = "YOUR_GEMINI_API_KEY"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/', methods=['POST'])
def google_chat_bot():
    event = request.json
    
    # בדיקה האם ההודעה הגיעה ממשתמש ב-Google Chat
    if event and 'message' in event:
        user_message = event['message']['text']
        
        # בניית הבקשה עבור Gemini API
        payload = {
            "contents": [{
                "parts": [{"text": user_message}]
            }]
        }
        
        response = requests.post(GEMINI_URL, json=payload)
        ai_response_text = "מצטער, אירעה שגיאה בעיבוד התשובה."
        
        if response.status_code == 200:
            data = response.json()
            try:
                ai_response_text = data['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError):
                pass
                
        # החזרת התשובה ל-Google Chat
        return jsonify({
            "text": ai_response_text
        })
        
    return jsonify({"text": "שלום! הבוט מחובר ומוכן לפעולה."})

if __name__ == '__main__':
    app.run(port=8080)
