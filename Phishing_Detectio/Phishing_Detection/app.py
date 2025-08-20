from flask import Flask, request, jsonify, render_template
import pickle
import re
import nltk
from nltk.corpus import stopwords
from flask_cors import CORS




# Load model and vectorizer
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# App
app = Flask(__name__)
CORS(app)

# Text cleaning function
def clean_email(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = ' '.join(word for word in text.split() if word not in stopwords.words('english'))
    return text

@app.route('/')
def home():
    return render_template('index.html')

# app = Flask(__name__, template_folder='front')

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/text-detection')
# def text_detection():
#     return render_template('text-detection.html')

    
    

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    email = data['email']
    cleaned = clean_email(email)
    vect = vectorizer.transform([cleaned])

    prediction = model.predict(vect)[0]
    proba = model.predict_proba(vect)[0]

    phishing_percent = round(proba[list(model.classes_).index('Phishing')] * 100, 2)

    # Red flags detection
    red_flags = []
    suspicious_keywords = ['urgent', 'verify', 'claim', 'click', 'win', 'suspend', 'account', 'secure', 'update', 'prize', 'gift', 'alert']
    email_lower = email.lower()

    for keyword in suspicious_keywords:
        if keyword in email_lower:
            red_flags.append(f"Keyword detected: '{keyword}'")

    if 'http' in email_lower or 'www' in email_lower:
        red_flags.append("Suspicious link detected.")
    
    if 'attachment' in email_lower or '.zip' in email_lower or '.exe' in email_lower:
        red_flags.append("Possible suspicious attachment mentioned.")

    return jsonify({
        'prediction': prediction,
        'phishing_probability': phishing_percent,
        'red_flags': red_flags
    })

   

    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
