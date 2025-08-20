from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import pandas as pd
import re
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')

# Load dataset
df = pd.read_csv('dataset.csv')  # you must have this CSV

# Cleaning function
def clean_email(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = ' '.join(word for word in text.split() if word not in stopwords.words('english'))
    return text

# Clean data
df['cleaned'] = df['Email Text'].apply(clean_email)

# Feature extraction
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['cleaned'])
y = df['Label']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# >>> Evaluate model here
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label='Phishing')
recall = recall_score(y_test, y_pred, pos_label='Phishing')
f1 = f1_score(y_test, y_pred, pos_label='Phishing')

print("\nModel Evaluation Metrics 📈:")
print(f"Accuracy : {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall   : {recall:.2f}")
print(f"F1 Score : {f1:.2f}\n")

# Save model and vectorizer

pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))

print("Training complete! 🚀")
