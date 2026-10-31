import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# =========================
# TRAINING EXAMPLES
# =========================

texts = [
    # LEARNING
    "I don't understand C++ loops",
    "I cannot understand pointers",
    "I am struggling to learn mathematics",
    "I don't understand functions in C",
    "I cannot solve programming questions",
    "I understand theory but cannot solve problems",
    "I am confused about recursion",
    "I don't understand integration",
    "I am having difficulty learning Python",
    "I keep making mistakes while coding",
    "I don't understand this topic",
    "I am weak in programming",
    "I don't understand how loops work",
    "I cannot solve C++ questions",
    "I am confused about pointers",
    "I don't understand recursion",
    "I am unable to understand integration",
    "I cannot understand mathematics",
    "I have difficulty understanding programming",
    "I don't know how to write code",
    "I understand the concept but cannot apply it",
    "I am struggling with coding",
    "I cannot solve practice questions",
    "I forget programming concepts",
    "I need help understanding this chapter",

    # DEADLINE
    "I have an exam tomorrow",
    "My project deadline is tomorrow",
    "I don't have enough time to finish my work",
    "My exam is next week",
    "I have too much work and very little time",
    "I have a deadline today",
    "I need to finish my project quickly",
    "My submission is due tomorrow",
    "I am running out of time",
    "My exam is coming soon",
    "I have very little time left",
    "My project is due tomorrow",
    "I need to submit my work today",
    "The deadline is very close",
    "I have an exam in two days",
    "I am late with my project",
    "I need to finish everything before tomorrow",
    "I have many tasks and no time",
    "My submission deadline is near",
    "I am worried about my upcoming exam",

    # ASSIGNMENT
    "I need to complete my assignment",
    "I have homework to submit",
    "I haven't completed my assignment",
    "I need help with my college assignment",
    "My assignment is pending",
    "I have an assignment to finish",
    "I don't know how to start my assignment",
    "I need to submit my homework",
    "My college assignment is incomplete",
    "I have not started my assignment",
    "I am stuck on my assignment",
    "I need to finish my homework",
    "My assignment work is pending",
    "I have to complete an assignment",
    "I don't know how to complete my homework",
    "I have a C++ assignment but don't understand loops",
    "I am confused about pointers in my college assignment",
    "I need help solving my programming homework",
    "I have to submit my assignment and cannot solve the questions",
    "I don't understand the topic required for my assignment",

    # GENERAL
    "I don't know how to manage my daily routine",
    "I am having a personal problem",
    "I don't know how to handle my situation",
    "I need help with a personal decision",
    "I am confused about what to do today",
    "I am having trouble managing my time",
    "I need guidance about my daily life",
    "I don't know how to deal with this situation",
    "I need help planning my daily routine",
    "I want to manage my daily schedule better",
    "I need advice about organizing my everyday tasks",
    "I am struggling to balance college and personal life",
    "I want to improve my time management habits",
]


# =========================
# TRAINING LABELS
# =========================

labels = (
    ["learning"] * 25
    + ["deadline"] * 20
    + ["assignment"] * 20
    + ["general"] * 13
)


# =========================
# TEXT PREPROCESSING
# =========================

def preprocess_text(text):
    text = text.lower()

    # Normalize common phrases
    text = text.replace("can't", "cannot")
    text = text.replace("unable to", "cannot")
    text = text.replace("don't understand", "do not understand")

    text = re.sub(r"[^a-z0-9+#\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =========================
# PREPARE TRAINING DATA
# =========================

processed_texts = [preprocess_text(text) for text in texts]

X_train_text, X_test_text, y_train, y_test = train_test_split(
    processed_texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)


# =========================
# CONVERT TEXT INTO FEATURES
# =========================

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=1000
)

X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)


# =========================
# TRAIN THE ML MODEL
# =========================

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


# =========================
# PREDICT CATEGORY
# =========================

def predict_category(problem):
    """Predict the category of a student's problem."""

    text = problem.lower()

    # Prioritize exam deadlines in mixed problems
    if any(word in text for word in [
        "exam", "deadline", "due tomorrow",
        "submission tomorrow", "test tomorrow"
    ]):
        return "deadline"

    processed_problem = preprocess_text(problem)
    problem_vector = vectorizer.transform([processed_problem])
    prediction = model.predict(problem_vector)[0]

    return prediction


# =========================
# TEST THE MODEL
# =========================

if __name__ == "__main__":
    test_problem = "I have a C++ assignment about loops"

    result = predict_category(test_problem)

    print("Test problem:", test_problem)
    print("Predicted category:", result)