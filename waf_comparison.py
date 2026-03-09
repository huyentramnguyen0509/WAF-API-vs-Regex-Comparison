import pandas as pd
import re
import time

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# =========================
# 1 LOAD DATASET
# =========================

df = pd.read_csv("csic_database.csv")

df["payload"] = df["URL"].fillna("") + " " + df["content"].fillna("")

X = df["payload"]
y = df["classification"]

# =========================
# 2 TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 3 TF-IDF FEATURE
# =========================

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1,2)
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# =========================
# 4 TRAIN RANDOM FOREST
# =========================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train_vec, y_train)

y_pred_ai = model.predict(X_test_vec)

print("===== Random Forest Model =====")

print("Accuracy:", accuracy_score(y_test, y_pred_ai))
print("Precision:", precision_score(y_test, y_pred_ai))
print("Recall:", recall_score(y_test, y_pred_ai))
print("F1:", f1_score(y_test, y_pred_ai))

# =========================
# 5 REGEX WAF
# =========================

patterns = [
    r"(?i)union\s+select",
    r"(?i)or\s+1=1",
    r"(?i)<script>",
    r"(?i)drop\s+table",
    r"(?i)insert\s+into",
    r"(?i)select\s+.*\s+from"
]

def regex_waf(payload):

    for p in patterns:
        if re.search(p, payload):
            return 1

    return 0


y_pred_regex = [regex_waf(x) for x in X_test]

print("\n===== Regex WAF =====")

print("Accuracy:", accuracy_score(y_test, y_pred_regex))
print("Precision:", precision_score(y_test, y_pred_regex))
print("Recall:", recall_score(y_test, y_pred_regex))
print("F1:", f1_score(y_test, y_pred_regex))

# =========================
# 6 BYPASS TEST
# =========================

print("\n===== Obfuscation Test =====")

payloads = [

    "' OR 1=1 --",
    "'/**/OR/**/1=1--",
    "' oR 1=1",

    "<script>alert(1)</script>",
    "<ScRiPt>alert(1)</sCrIpT>",
]

for p in payloads:

    regex_result = regex_waf(p)

    vec = vectorizer.transform([p])
    ai_result = model.predict(vec)[0]

    print("\nPayload:", p)
    print("Regex:", regex_result)
    print("AI:", ai_result)

# =========================
# 7 LATENCY TEST
# =========================

print("\n===== Latency Test =====")

test_payload = X_test.iloc[0]

start = time.time()
regex_waf(test_payload)
end = time.time()

regex_latency = (end-start)*1000

vec = vectorizer.transform([test_payload])

start = time.time()
model.predict(vec)
end = time.time()

ai_latency = (end-start)*1000

print("Regex latency:", regex_latency, "ms")
print("AI latency:", ai_latency, "ms")