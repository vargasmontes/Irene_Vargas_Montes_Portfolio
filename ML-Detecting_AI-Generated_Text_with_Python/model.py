import kagglehub
import os
import pandas as pd

import nltk
from nltk.corpus import stopwords
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Find the dataset from KaggleHub
path = kagglehub.dataset_download("alitaqishah/ai-vs-human-text-classification-dataset-2026")
data_file = os.path.join(path, os.listdir(path)[0])
df = pd.read_csv(data_file)

# Clean the text from the dataset
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = [i for i in text.split() if i not in stop_words]
    return ' '.join(words)

df['clean_text'] = df['text_content'].astype(str).apply(clean_text)

# Making the labels binary and cleaning duplicates
df['label_binary'] = df['label'].map({'human': 0, 'ai': 1})
df = df.drop_duplicates(subset=['clean_text'])

# TF-IDF and Training
X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['label_binary'], test_size=0.2, random_state=42, stratify=df['label_binary'])

vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Evaluate
y_pred = model.predict(X_test_tfidf)
print("\nClassification Report")
print(classification_report(y_test, y_pred, target_names=['Human', 'AI']))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Human','AI'], yticklabels=['Human','AI'])
plt.xlabel('Predicted'); plt.ylabel('Actual'); plt.title('Confusion Matrix')
plt.show()

# Test outside the Dataset
new_samples = ["Artificial intelligence is for sure the future, but we need to use it in the right way. ", "Artificial intelligence (AI) is a field of computer science focused on creating systems that can perform tasks that typically require human intelligence, such as recognizing patterns, understanding language, and making decisions. "]
new_clean = [clean_text(t) for t in new_samples]
new_tfidf = vectorizer.transform(new_clean)

predictions = model.predict(new_tfidf)
label_map = {0: 'Human', 1: 'AI'}

print("\nExternal Test Results")
for text, pred in zip(new_samples, predictions):
    print(f"Text: \"{text[:80]}...\"")
    print(f"Predicted: {label_map[pred]}\n")
