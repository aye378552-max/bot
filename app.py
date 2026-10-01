from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = "הכנס_כאן_את_המפתח_שלך"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/', methods=['POST'])
def google_chat_bot():
    event = request.json
    print("Received event:", event) # עוזר לראות בלוגים מה גוגל שולח בדיוק
    
    user_message = ""
    
    # חילוץ ההודעה בהתאם למבנה שמגיע מ-Google Chat
    if event:
        if 'message' in event:
            user_message = event['message'].get('text', '')
        elif 'text' in event:
            user_message = event['text']
            
    if not user_message:
        # אם אין טקסט ספציפי, נחזיר הודעת פתיחה ברורה
        return jsonify({"text": "שלום! הבוט מחובר ומוכן לפעולה."})
        
    # בניית הבקשה עבור Gemini API
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }
    
    try:
        response = requests.post(GEMINI_URL, json=payload)
        ai_response_text = "מצטער, אירעה שגיאה בעיבוד התשובה מ-Gemini."
        
        if response.status_code == 200:
            data = response.json()
            try:
                ai_response_text = data['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError):
                pass
        else:
            ai_response_text = f"שגיאת תקשורת מול גוגל (קוד {response.status_code})"
    except Exception as e:
        ai_response_text = f"שגיאה פנימית בשרת: {str(e)}"
        
    # החזרת התשובה במבנה המדויק שגוגל צ'אט דורש
    return jsonify({
        "text": ai_response_text
    })

if __name__ == '__main__':
    app.run(port=8080)
