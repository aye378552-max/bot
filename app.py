from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# הכנס כאן את מפתח ה-API שלך מ-Google AI Studio
GEMINI_API_KEY = "הכנס_כאן_את_המפתח_שליך"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/', methods=['POST'])
def google_chat_bot():
    event = request.json
    print("Received event:", event)
    
    user_message = ""
    
    if event:
        # חילוץ הטקסט מתוך המבנה של Google Chat / Workspace Add-ons
        if 'commonEventObject' in event and 'parameters' in event['commonEventObject']:
            user_message = event['commonEventObject']['parameters'].get('text', '')
            
        if not user_message and 'message' in event:
            user_message = event['message'].get('text', '')
            
        if not user_message and 'text' in event:
            user_message = event['text']
            
    # אם לא נמצא טקסט בהודעה, נציג ברירת מחדל
    if not user_message:
        user_message = "שלום!"

    # בניית הבקשה עבור Gemini API
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
        else:
            ai_response_text = f"שגיאת תקשורת מול גוגל (קוד {response.status_code})"
    except Exception as e:
        ai_response_text = f"שגיאה: {str(e)}"
        
    # החזרת התשובה בפורמט המלא לגוגל צ'אט
    return jsonify({
        "text": ai_response_text
    }), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(port=8080)
