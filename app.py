from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = "הכנס_כאן_את_המפתח_שליך"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/', methods=['POST'])
def google_chat_bot():
    event = request.json
    
    user_message = ""
    
    if event:
        # בדיקה אם ההודעה מגיעה במבנה של Google Workspace Add-on / Google Chat חדש
        if 'commonEventObject' in event and 'parameters' in event['commonEventObject']:
            user_message = event['commonEventObject']['parameters'].get('text', '')
            
        # בדיקה אם ההודעה מגיעה כמבנה הודעה ישיר
        if not user_message and 'message' in event:
            user_message = event['message'].get('text', '')
            
        # בדיקה בנתיבים חלופיים
        if not user_message and 'text' in event:
            user_message = event['text']
            
    # אם עדיין לא נמצא טקסט, ננסה לחלץ מתוך הטקסט של האירוע או שנחזיר תגובת בדיקה שמציגה שהבוט מחובר
    if not user_message:
        user_message = "שלום, אנא אמור לי במה תרצה עזרה."

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
    except Exception as e:
        ai_response_text = f"שגיאה: {str(e)}"
        
    return jsonify({
        "text": ai_response_text
    })

if __name__ == '__main__':
    app.run(port=8080)
