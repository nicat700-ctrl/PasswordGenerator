# Phishing Email Detector 🎯

Python ilə hazırlanmış, Machine Learning (TF-IDF + Logistic Regression) əsaslı
phishing e-mail aşkarlama proqramı.

## Xüsusiyyətlər
- E-mail mətnini analiz edir
- "phishing" və "legitimate" olaraq təsnif edir
- Hər proqnoz üçün ehtimal faizini göstərir
- Terminal üzərindən interaktiv test rejimi

## Qurulum

```bash
git clone https://github.com/<istifadeci-adiniz>/phishing-email-detector.git
cd phishing-email-detector
pip install -r requirements.txt
```

## İstifadə

Modeli öyrətmək:
```bash
python phishing_detector.py train
```

Tək e-maili yoxlamaq:
```bash
python phishing_detector.py predict "Your account will be suspended, click here to verify"
```

İnteraktiv rejim (bir neçə email ardıcıl yoxlamaq üçün):
```bash
python phishing_detector.py interactive
```

## Fayl strukturu
```
phishing-email-detector/
├── phishing_detector.py   # əsas proqram
├── data.csv               # nümunə təlim datası
├── requirements.txt       # asılılıqlar
└── README.md
```

## Model haqqında
- **Vektorlaşdırma:** TF-IDF (1-2 gram)
- **Təsnifatçı:** Logistic Regression
- **Dataset:** `data.csv` faylındakı nümunə e-maillər (öz datanızla əvəz edə bilərsiniz, məsələn Kaggle-dəki "Phishing Email Dataset")

> Qeyd: Daxil olan `data.csv` kiçik nümunə datasetdir. Daha yüksək dəqiqlik üçün
> böyük real dataset (məsələn Kaggle-də "Phishing Email Detection Dataset") istifadə edin.
