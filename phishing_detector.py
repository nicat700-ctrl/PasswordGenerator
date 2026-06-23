"""
Phishing Email Detector
------------------------
TF-IDF + Logistic Regression istifadə edərək e-mail mətnini analiz edir
və phishing (saxta/zərərli) olub-olmadığını proqnozlaşdırır.

İstifadə:
    python phishing_detector.py train      -> modeli öyrədir və yadda saxlayır
    python phishing_detector.py test        -> test datası üzərində nəticələri göstərir
    python phishing_detector.py predict "email mətni"   -> tək e-maili yoxlayır
    python phishing_detector.py interactive -> terminal üzərindən maraqlı e-mailləri yoxla
"""

import sys
import re
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

MODEL_PATH = "phishing_model.joblib"
DATA_PATH = "data.csv"


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " URL ", text)
    text = re.sub(r"[^a-zçğıöşü0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["text_clean"] = df["text"].apply(clean_text)
    return df


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")),
        ("clf", LogisticRegression(max_iter=1000)),
    ])


def train():
    df = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        df["text_clean"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("\n=== Model Performansı ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}\n")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nModel '{MODEL_PATH}' faylına yadda saxlanıldı.")


def load_model() -> Pipeline:
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print("Model tapılmadı. Əvvəlcə 'python phishing_detector.py train' işlədin.")
        sys.exit(1)


def predict_email(text: str):
    model = load_model()
    cleaned = clean_text(text)
    pred = model.predict([cleaned])[0]
    proba = model.predict_proba([cleaned])[0]
    classes = model.classes_
    prob_dict = dict(zip(classes, proba))

    print("\n--- Nəticə ---")
    print(f"E-mail: {text[:80]}{'...' if len(text) > 80 else ''}")
    print(f"Proqnoz: {pred.upper()}")
    for c in classes:
        print(f"  {c}: {prob_dict[c]*100:.1f}%")
    return pred, prob_dict


def interactive():
    load_model()  # ensure exists, errors early if not
    print("Çıxmaq üçün 'exit' yazın.")
    while True:
        text = input("\nE-mail mətnini daxil edin: ")
        if text.strip().lower() == "exit":
            break
        predict_email(text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("İstifadə: python phishing_detector.py [train|predict|interactive] [\"mətn\"]")
        sys.exit(0)

    command = sys.argv[1]

    if command == "train":
        train()
    elif command == "predict":
        if len(sys.argv) < 3:
            print("Zəhmət olmasa mətn daxil edin: python phishing_detector.py predict \"email text\"")
            sys.exit(1)
        predict_email(sys.argv[2])
    elif command == "interactive":
        interactive()
    else:
        print(f"Naməlum əmr: {command}")
