from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import re

# ==============================
#       NLP PREPROCESSING
# ==============================

def preprocess_text(text):
    text = text.lower()

    # Normalize common phrases
    text = text.replace("can't", "cannot")
    text = text.replace("unable to", "cannot")
    text = text.replace("don't understand", "do not understand")

    text = re.sub(r"[^a-z0-9+#\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

# ==============================
#       SESSION MEMORY
# ==============================

previous_problem = None
previous_subject = None
previous_topic = None
previous_stress = None
previous_learning_gap = None
previous_priority = None

# Training examples
texts = [

    # =========================
    # LEARNING
    # =========================

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

    # =========================
    # DEADLINE
    # =========================

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

    # =========================
    # ASSIGNMENT
    # =========================

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

    # =========================
    # GENERAL
    # =========================

"I don't know how to manage my daily routine",
"I am having a personal problem",
"I don't know how to handle my situation",
"I need help with a personal decision",
"I am confused about what to do today",
"I am having trouble managing my time",
"I need guidance about my daily life",
"I don't know how to deal with this situation",
]

labels = [

    # Learning - 25
    "learning", "learning", "learning", "learning", "learning",
    "learning", "learning", "learning", "learning", "learning",
    "learning", "learning", "learning", "learning", "learning",
    "learning", "learning", "learning", "learning", "learning",
    "learning", "learning", "learning", "learning", "learning",

    # Deadline - 20
    "deadline", "deadline", "deadline", "deadline", "deadline",
    "deadline", "deadline", "deadline", "deadline", "deadline",
    "deadline", "deadline", "deadline", "deadline", "deadline",
    "deadline", "deadline", "deadline", "deadline", "deadline",

    # Assignment - 15
    "assignment", "assignment", "assignment", "assignment", "assignment",
    "assignment", "assignment", "assignment", "assignment", "assignment",
    "assignment", "assignment", "assignment", "assignment", "assignment",

    # General - 8
   "general", "general", "general", "general", 
   "general", "general", "general", "general", 
]

# Preprocess all training examples first
processed_texts = [preprocess_text(text) for text in texts]

# Split the preprocessed data
X_train_text, X_test_text, y_train, y_test = train_test_split(
    processed_texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)

# Convert text into numerical features
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=1000
)

X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)

# Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("\n==============================")
print("       Model Evaluation")
print("==============================")
print("Test Accuracy:", round(accuracy * 100, 2), "%")# Detailed Classification Report

y_pred = model.predict(X_test)

print("\n==============================")
print("   Classification Report")
print("==============================")

print(classification_report(y_test, y_pred, zero_division=0))

print("\n==============================")
print("   Prediction Details")
print("==============================")

for text, actual, predicted in zip(X_test_text, y_test, y_pred):
    print("\nInput:", text)
    print("Actual:", actual)
    print("Predicted:", predicted)

# ==========================================
# GET STUDENT PROBLEM
# ==========================================

while True:

    problem = input("\nTell me your problem (type 'exit' to stop):")

    if problem.lower() == "exit":
        print("\nSession ended.")
        break

    # PREPROCESS STUDENT INPUT
    text = preprocess_text(problem)

    # CONVERT STUDENT PROBLEM INTO NUMBERS
    problem_vector = vectorizer.transform([text])

    # Predict primary problem category
    prediction = model.predict(problem_vector)

    primary_problem = prediction[0]

    # ==============================
    #       NLP INTENT
    # ==============================

    if (
        "can't solve" in text
        or "cannot solve" in text
        or "don't understand" in text
        or "confused" in text
    ):
        intent = "Learning Difficulty"

    elif (
        "exam" in text
        or "deadline" in text
        or "tomorrow" in text
    ):
        intent = "Deadline / Exam"

    elif (
        "assignment" in text
        or "homework" in text
    ):
        intent = "Assignment"

    else:
        intent = primary_problem
    print("intent:", intent)

    # Convert input to lowercase
    text = problem.lower()

    # ==========================================
    # USE SESSION MEMORY FOR VAGUE FOLLOW-UPS
    # ==========================================

    vague_followup_words = [
        "same problem",
        "same thing",
        "still stuck",
        "still struggling",
        "this problem",
        "still confused",
        "i don't understand it",
        "i still don't understand"
    ]

    if previous_problem is not None and any(
        phrase in text for phrase in vague_followup_words
    ):
        print("\nContinuing from your previous problem...")

        if previous_subject != "Not identified":
            subject = previous_subject

        if previous_topic != "Not identified":
            topic = previous_topic

   



    # ==========================================
    # MULTI-PROBLEM DETECTION
    # ==========================================

    detected_problems = []

    # Continue previous learning problem
    if (
        previous_problem is not None
        and any(
            phrase in text
            for phrase in [
                "same problem",
                "same thing",
                "still stuck",
                "still struggling",
                "this problem"
            ]
        )
        and previous_learning_gap == "Concept application"
    ):
        detected_problems.append(("Learning Difficulty", 3))

    # Deadline / Exam detection
    if (
        "exam" in text
        or "tomorrow" in text
        or "deadline" in text
        or "today" in text
    ):
        detected_problems.append(("Exam / Deadline", 4))


    # Learning difficulty detection
    if (
        "understand" in text
        or "confused" in text
        or "cannot solve" in text
        or "can't solve" in text
        or "struggling" in text
        or "question" in text
        or "questions" in text
    ):

        detected_problems.append(("Learning Difficulty", 3))


    # Assignment detection
    if "assignment" in text or "homework" in text:
        detected_problems.append(("Assignment", 2))


    # Store only problem names
    problem_names = [name for name, score in detected_problems]


    # ==========================================
    # CRISIS2CLARITY AI
    # ==========================================

    print("\n==============================")
    print("       Crisis2Clarity AI")
    print("==============================")

    print("Primary Problem:", primary_problem.capitalize())


    # Convert ML category into display name
    primary_display = {
        "deadline": "Exam / Deadline",
        "learning": "Learning Difficulty",
        "assignment": "Assignment",
        "general": "General"
    }.get(primary_problem, primary_problem)


    # Show other detected problems
    other_problems = [
        name for name in problem_names
        if name != primary_display
    ]

    if other_problems:

        print("\nOther Problems Detected:")

        for name in other_problems:
            print("-", name)


    # ==========================================
    # SUGGESTED ACTION
    # ==========================================

    if primary_problem == "learning":

        print("\nSuggested Action:")

        print("1. Identify the exact topic you are struggling with.")
        print("2. Review the basic concept.")
        print("3. Solve 3-5 simple practice questions.")
        print("4. Try the problem again.")


    elif primary_problem == "deadline":

        print("\nSuggested Action:")

        print("1. Identify the most urgent task.")
        print("2. Break it into smaller tasks.")
        print("3. Complete the highest-priority task first.")
        print("4. Set a short deadline for each task.")


    elif primary_problem == "assignment":

        print("\nSuggested Action:")

        print("1. Read the assignment requirements.")
        print("2. Break the assignment into smaller parts.")
        print("3. Complete one part at a time.")
        print("4. Review your work before submission.")


    else:

        print("\nSuggested Action:")

        print("1. Describe the problem clearly.")
        print("2. Identify what is causing the difficulty.")
        print("3. Decide what needs to be done first.")


    # ==========================================
    # LEARNING GAP DETECTION
    # ==========================================

    if "Learning Difficulty" in problem_names:

        print("\n==============================")
        print("       Learning Gap")
        print("==============================")

        if (
            previous_learning_gap == "Concept application"
            and previous_problem is not None
            and "still" in text
            and "understand" in text
        ):

            gap = "Concept application"

            gap_action = (
                "Continue practicing the concept and solve "
                "3-5 targeted questions."
            )

        elif (
            "understand" in text
            and (
                "how to start" in text
                or "where to start" in text
                or "approach" in text
                or "how to solve" in text
            )
        ):

            gap = "Problem-solving approach"

            gap_action = (
                "Learn a step-by-step approach and practice "
                "solving similar problems."
            )

        elif (
            "theory" in text
            and (
                "code" in text
                or "coding" in text
                or "program" in text
                or "programming" in text
            )
        ):

            gap = "Applying theory to coding"

            gap_action = (
                "Connect the theory to a small coding example "
                "and practice 3-5 related programs."
            )   

        elif (
            ("understand" in text or "cannot solve" in text)
            and (
                "solve" in text
                or "problem" in text
                or "question" in text
                or "questions" in text
            )
        ):

            gap = "Concept application"

            gap_action = (
                "Review the basic concept and solve "
                "3-5 simple practice questions."
            )
        
        elif "remember" in text or "forget" in text:

            gap = "Concept retention"

            gap_action = (
                "Use active recall and revise the concept."
            )

        elif "confused" in text:

            gap = "Concept clarity"

            gap_action = (
                "Break the topic into smaller concepts "
                "and learn them one at a time."
            )

        else:

            gap = "Concept clarity"

            gap_action = (
                "Identify the exact topic and review "
                "its basic concepts."
            )

        print("Possible Learning Gap:", gap)
        print("Learning Action:", gap_action)

    # ==========================================
    # PRIORITY ANALYSIS
    # ==========================================

    priority_score = 0

    for name, score in detected_problems:

        priority_score += score


    if priority_score == 0:

        priority_score = 1


    if priority_score > 10:

        priority_score = 10


    # Determine urgency
    if priority_score >= 8:

        urgency = "Very High"

    elif priority_score >= 5:

        urgency = "High"

    elif priority_score >= 3:

        urgency = "Medium"

    else:

        urgency = "Low"


    print("\n==============================")
    print("       Problem Analysis")
    print("==============================")


    if detected_problems:

        print("Problems detected:")

        for name, score in detected_problems:

            print("-", name)

    else:

        print("No specific problems detected.")


    print("\nPriority Score:", str(priority_score) + "/10")

    print("Urgency:", urgency)

    # ==========================================
    # STRESS LEVEL DETECTION
    # ==========================================

    stress_words = [
        "stressed",
        "stress",
        "worried",
        "anxious",
        "anxiety",
        "overwhelmed",
        "pressure",
        "panic",
        "tension",
        "scared",
        "afraid",
        "frustrated",
        "exhausted",
        "burnout",
        "exam tomorrow",
        "deadline tomorrow",
        "can't finish",
        "cannot finish",
        "too much work",
        "lots of work",
        "still pending",
        "running out of time"
]

   
    stress_count = 0

    for word in stress_words:
        if word in text:
            stress_count += 1


    if stress_count >= 3:
        stress_level = "Very High"

    elif stress_count >= 2:
        stress_level = "High"

    elif stress_count == 1:
        stress_level = "Moderate"

    else:
        stress_level = "Low"


    print("\n==============================")
    print("       Stress Analysis")
    print("==============================")

    print("Stress Level:", stress_level)


    if stress_level == "Very High":

        print("Recommendation:")
        print("1. Pause and take a short break.")
        print("2. Focus on one urgent task at a time.")
        print("3. Avoid trying to complete everything at once.")

    elif stress_level == "High":

        print("Recommendation:")
        print("1. Break your work into smaller tasks.")
        print("2. Start with the most urgent task.")
        print("3. Take short breaks between study sessions.")

    elif stress_level == "Moderate":

        print("Recommendation:")
        print("1. Make a simple plan.")
        print("2. Focus on one task at a time.")
        print("3. Take a short break if needed.")

    else:

        print("Recommendation:")
        print("Continue with your planned study/action steps.")

    
    # Personalized Action Plan

    print("\n==============================")
    print("   Personalized Action Plan")
    print("==============================")

    problem_names = [name for name, score in detected_problems]

    if "Exam / Deadline" in problem_names and "Learning Difficulty" in problem_names:

        print("1. Focus on the most important exam topic first.")
        print("2. Review the basic C++ concepts you don't understand.")
        print("3. Solve 3 basic practice questions.")
        print("4. Solve 2 exam-level questions.")
        print("5. Review your mistakes.")

    elif "Exam / Deadline" in problem_names:

        print("1. Identify the task with the nearest deadline.")
        print("2. Break it into smaller tasks.")
        print("3. Complete the most important task first.")
        print("4. Set a short time limit for each task.")
        print("5. Review your work before submission.")

    elif "Learning Difficulty" in problem_names:

        print("1. Identify the exact topic you are struggling with.")
        print("2. Review the basic concept.")
        print("3. Solve 3-5 simple practice questions.")
        print("4. Check your mistakes.")
        print("5. Try the problem again.")

    elif "Assignment" in problem_names:

        print("1. Read the assignment requirements.")
        print("2. Divide the assignment into smaller sections.")
        print("3. Complete one section at a time.")
        print("4. Review your answers.")
        print("5. Prepare the final submission.")

    else:

        print("1. Clearly identify the main problem.")
        print("2. Break the problem into smaller steps.")
        print("3. Complete the most important step first.")
        print("4. Review your progress.")

        # Reassessment System

    print("\n==============================")
    print("        Reassessment")
    print("==============================")

    feedback = input(
        "\nDid this action plan help you?\n"
        "1. Yes, I understand now\n"
        "2. Partially, I still have difficulty\n"
        "3. No, I am still stuck\n"
        "Enter your choice: "
    )

    if feedback == "1":
        print("\nGreat! 🎉")
        print("You can now try a slightly harder problem.")

    elif feedback == "2":
        print("\nLet's go one step deeper.")
        print("Identify the exact part that is still difficult.")
        print("Then practice that specific concept again.")

    elif feedback == "3":
        print("\nLet's reassess the problem.")
        print("Try explaining what you attempted and where you got stuck.")
        print("Crisis2Clarity can then create a new action plan.")

    else:
        print("\nPlease enter 1, 2, or 3.")

                # Subject and Topic Detection

    text = problem.lower()

    # ==========================================
    #          SESSION MEMORY CHECK
    # ==========================================

    

    subject = "General"
    topic = "Not identified"

    # Carry forward previous context for vague follow-ups
    if (
        previous_problem is not None
        and any(
            phrase in text
            for phrase in [
                "still don't understand it",
                "i don't understand it",
                "still confused",
                "same problem",
                "same thing",
                "still stuck",
                "still struggling",
                "this problem"
            ]
        )
    ):
        subject = previous_subject
        topic = previous_topic

    if "c++" in text or "cpp" in text or "cplusplus" in text:
        subject = "C++"

        if "loop" in text or "loops" in text:
            topic = "Loops"
        elif (
            "pointer" in text
            or "pointers" in text
            or "address" in text
            or "dereference" in text
        ):
            topic = "Pointers"
        elif (
            "recursion" in text
            or "recursive" in text
            or "recursive function" in text
            or "base case" in text
        ):
            topic = "Recursion"
        elif (
            "function" in text
            or "functions" in text
            or "parameter" in text
            or "parameters" in text
            or "return value" in text
        ):
            topic = "Functions"
        
        else:
            topic = "Programming"

    elif "python" in text:
        subject = "Python"

        if (
            "loop" in text
            or "loops" in text
            or "iteration" in text
            or "for loop" in text
            or "while loop" in text
        ):
            topic = "Loops"

        elif (
            "function" in text
            or "functions" in text
            or "parameter" in text
            or "parameters" in text
            or "return value" in text
        ):
            topic = "Functions"

        else:
            topic = "Programming"

    elif "math" in text or "mathematics" in text:
        subject = "Mathematics"

        if "integration" in text:
            topic = "Integration"
        elif "derivative" in text or "differentiation" in text:
            topic = "Differentiation"
        elif "matrix" in text or "matrices" in text:
            topic = "Matrices"
        else:
            topic = "Mathematics"

    elif "electronics" in text or "diode" in text:
        subject = "Electronics"

        if "pn junction" in text or "pn-junction" in text:
            topic = "PN Junction Diode"
        elif "rectifier" in text:
            topic = "Rectifier"
        else:
            topic = "Electronics"


    print("\n==============================")
    print("     Subject & Topic")
    print("==============================")

    print("Subject:", subject)
    print("Topic:", topic)


    # ==========================================
    #          SESSION MEMORY CHECK
    # ==========================================

    if previous_problem is not None:

        print("\n==============================")
        print("       Session Memory")
        print("==============================")

        print("Previous Problem:", previous_problem)
        print("Previous Subject:", previous_subject)
        print("Previous Topic:", previous_topic)
        print("Previous Stress:", previous_stress)
        print("Previous Learning Gap:", previous_learning_gap)
        print("Previous Priority:", str(previous_priority) + "/10")

        if (
            previous_subject == subject
            and previous_topic == topic
            and topic != "Not identified"
        ):
            print("\nContinuing Topic:", previous_subject, "-", previous_topic)
            print("This appears to be a continuing problem.")
        else:
            print("\nThis appears to be a new problem.")


    # Topic-Specific Recommendation

        print("\n==============================")
        print("       Topic-Specific Guidance")
        print("==============================")

    if subject == "C++" and topic == "Loops":

        print("Topic: C++ Loops")
        print("\nWhich part of C++ loops is difficult?")
        print("1. for loop")
        print("2. while loop")
        print("3. do-while loop")
        print("4. Nested loops")
        print("5. Pattern questions")

        loop_choice = input("Enter your choice: ")

        if loop_choice == "1":

            print("\nFocus: for loop")
            print("1. Revise initialization, condition, and update.")
            print("2. Practice 3 simple for-loop programs.")
            print("3. Solve 2 exam-level questions.")

        elif loop_choice == "2":

            print("\nFocus: while loop")
            print("1. Revise the while-loop condition.")
            print("2. Practice 3 simple while-loop programs.")
            print("3. Solve 2 exam-level questions.")

        elif loop_choice == "3":

            print("\nFocus: do-while loop")
            print("1. Revise the do-while structure.")
            print("2. Understand why it executes at least once.")
            print("3. Solve 3 practice questions.")

        elif loop_choice == "4":

            print("\nFocus: Nested loops")
            print("1. Understand outer and inner loops.")
            print("2. Trace nested loops step by step.")
            print("3. Practice 3 nested-loop problems.")

        elif loop_choice == "5":

            print("\nFocus: Pattern questions")
            print("1. Practice rows and columns.")
            print("2. Trace the outer and inner loops.")
            print("3. Solve 3 basic pattern problems.")

        else:

            print("\nInvalid choice.")
            print("Start with for, while, and do-while loops.")

    elif subject == "C++" and topic == "Pointers":

        print("Topic: C++ Pointers")
        print("Recommended Practice:")
        print("1. Revise pointer basics.")
        print("2. Understand address and dereferencing.")
        print("3. Practice simple pointer programs.")
        print("4. Solve 3 pointer-based problems.")

    elif subject == "C++" and topic == "Functions":

        print("Topic: C++ Functions")
        print("Recommended Practice:")
        print("1. Revise function declaration and definition.")
        print("2. Practice parameters and return values.")
        print("3. Practice function-based programs.")
        print("4. Solve 3 problems using functions.")

    elif subject == "C++" and topic == "Recursion":

        print("Topic: C++ Recursion")
        print("Recommended Practice:")
        print("1. Understand the base case.")
        print("2. Understand recursive calls.")
        print("3. Trace a simple recursive function.")
        print("4. Practice factorial and Fibonacci problems.")

    elif subject == "Python" and topic == "Loops":

        print("Topic: Python Loops")
        print("Recommended Practice:")
        print("1. Revise for and while loops.")
        print("2. Practice nested loops.")
        print("3. Solve 3 basic loop problems.")
        print("4. Practice one small coding problem.")

    elif subject == "Mathematics" and topic == "Integration":

        print("Topic: Integration")
        print("Recommended Practice:")
        print("1. Revise important integration identities.")
        print("2. Practice basic integration problems.")
        print("3. Practice substitution-based questions.")
        print("4. Solve 3 exam-level problems.")

    elif subject == "Electronics" and topic == "PN Junction Diode":

        print("Topic: PN Junction Diode")
        print("Recommended Practice:")
        print("1. Revise PN junction formation.")
        print("2. Understand forward and reverse bias.")
        print("3. Revise the V-I characteristics.")
        print("4. Practice drawing and explaining the graph.")

    else:

        print("No topic-specific guidance available yet.")
        print("Try describing the exact topic you are struggling with.")

    # ==============================
    #       SAVE SESSION MEMORY
    # ==============================
    
    previous_problem = problem
    previous_subject = subject
    previous_topic = topic
    previous_stress = stress_level
    previous_learning_gap = locals().get("gap", "Not identified")
    previous_priority = priority_score
    