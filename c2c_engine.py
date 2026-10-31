def analyze_problem(problem):
    text = problem.lower().strip()

    if not text:
        return {
            "problem": "No input",
            "intent": "Not identified",
            "learning_gap": "Not identified",
            "next_step": "Please describe your problem.",
            "priority": 0,
            "urgency": "Not identified"
        }

    # Detect multiple problem categories
    detected_intents = []

    if any(word in text for word in [
        "exam", "deadline", "tomorrow", "submission due"
    ]):
        detected_intents.append("Deadline / Exam")

    if any(word in text for word in [
        "assignment", "homework"
    ]):
        detected_intents.append("Assignment")

    if any(phrase in text for phrase in [
        "don't understand",
        "do not understand",
        "cannot understand",
        "can't understand",
        "confused",
        "cannot solve",
        "can't solve",
        "struggling to learn",
        "difficulty learning",
        "difficulty understanding"
    ]):
        detected_intents.append("Learning Difficulty")

        # Detect additional student problems

    if any(word in text for word in [
        "stress", "stressed", "anxiety", "anxious",
        "exam fear", "nervous"
    ]):
        detected_intents.append("Stress / Anxiety")

    if any(word in text for word in [
        "time management", "no time", "manage time",
        "time shortage", "poor schedule"
    ]):
        detected_intents.append("Time Management")

    if any(word in text for word in [
        "procrastination", "procrastinating",
        "procrastinate", "keep delaying"
    ]):
        detected_intents.append("Procrastination")

    if any(word in text for word in [
        "cannot concentrate", "can't concentrate",
        "lack of concentration", "distracted",
        "difficulty focusing"
    ]):
        detected_intents.append("Concentration Difficulty")

    if any(word in text for word in [
        "no motivation", "lack of motivation",
        "demotivated", "not motivated"
    ]):
        detected_intents.append("Low Motivation")

    if not detected_intents:
        intent = "General"
    else:
        intent = detected_intents[0]

    gap = "Not identified"
    gap_action = "Describe the exact topic you find difficult."

    if "loop" in text:
        gap = "Understanding loops"
        gap_action = (
            "Review initialization, condition, and update. "
            "Then solve one simple loop question."
        )
    elif "pointer" in text:
        gap = "Understanding pointers"
        gap_action = (
            "Review memory addresses and pointer variables. "
            "Then trace a small example."
        )
    elif "function" in text:
        gap = "Understanding functions"
        gap_action = (
            "Review function definition, arguments, and return values. "
            "Then write one simple function."
        )
    elif "array" in text:
        gap = "Understanding arrays"
        gap_action = (
            "Review array indexing and element access. "
            "Then write a program to store and print five numbers."
        )
    elif "string" in text:
        gap = "Understanding strings"
        gap_action = (
            "Review string declaration and character access. "
            "Then write a program to find the length of a string."
        )
    elif "recursion" in text:
        gap = "Understanding recursion"
        gap_action = (
            "Review the base case and recursive call. "
            "Then trace a factorial example."
        )
    elif "data type" in text:
        gap = "Understanding data types"
        gap_action = (
            "Review basic, derived, and user-defined data types. "
            "Then identify the data type used in simple examples."
        )

    # Generate topic-specific guidance
    if "loop" in text:
        topic_guidance = [
            "Review for, while, and do-while loops.",
            "Trace the loop variable through each iteration.",
            "Write a program to print numbers from 1 to 10."
        ]
    elif "pointer" in text:
        topic_guidance = [
            "Review variables and memory addresses.",
            "Understand the address-of (&) and dereference (*) operators.",
            "Trace a pointer example step by step."
        ]
    elif "function" in text:
        topic_guidance = [
            "Review function definitions and parameters.",
            "Practise function calls and return values.",
            "Write a function to calculate a number's square."
        ]
    elif "array" in text:
        topic_guidance = [
            "Understand array indexing and positions.",
            "Practise accessing and updating array elements.",
            "Write a program to find the largest array element."
        ]
    elif "string" in text:
        topic_guidance = [
            "Learn string declaration and initialization.",
            "Practise accessing individual characters.",
            "Write a program to calculate string length."
        ]
    elif "recursion" in text:
        topic_guidance = [
            "Understand the base case.",
            "Trace recursive function calls.",
            "Write a factorial program using recursion."
        ]
    elif "data type" in text:
        topic_guidance = [
            "Review basic, derived, and user-defined data types.",
            "Understand the purpose of each data type.",
            "Practise selecting suitable data types."
        ]
    elif intent == "Deadline / Exam":
        topic_guidance = [
            "Identify important topics for the upcoming exam.",
            "Revise key formulas and concepts.",
            "Practise questions under a time limit."
        ]
    else:
        topic_guidance = [
            "Write down your main responsibilities for today.",
            "Separate urgent tasks from tasks that can wait.",
            "Use a realistic daily schedule."
        ]

     # Calculate problem priority
    priority = 3
    text_lower = text.lower()

    if "tomorrow" in text_lower or "exam" in text_lower:
        priority = 9
    elif "deadline" in text_lower or "due soon" in text_lower:
        priority = 7
    elif "assignment" in text_lower or "homework" in text_lower:
        priority = 5
    elif intent == "Learning Difficulty":
        priority = 4

    if priority >= 8:
        urgency = "High"
    elif priority >= 5:
        urgency = "Medium"
    else:
        urgency = "Low"

    return {
        "problem": problem,
        "intent": intent,
        "detected_intents":
         detected_intents,
        "learning_gap": gap,
        "next_step": gap_action,
        "priority": priority,
        "urgency": urgency,
      "action_plan": (
            (
                [
                    "Step 1 (5 min): Read the assignment questions carefully.",
                    "Step 2 (10 min): Identify the topics and concepts required."
                ]
                if "Assignment" in detected_intents else []
            )
            +
            (
                [
                    "Step 3 (10 min): Review the basic concept of the difficult topic.",
                    "Step 4 (15 min): Solve one easy example step by step.",
                    "Step 5 (20 min): Try two similar questions independently."
                ]
                if "Learning Difficulty" in detected_intents else []
            )
            +
            (
                [
                    "Step 6 (10 min): Prioritize the work due tomorrow.",
                    "Step 7 (25 min): Complete the most urgent task first.",
                    "Step 8 (5 min): Review your progress."
                ]
                if "Deadline / Exam" in detected_intents else []
            )
            if detected_intents
            else [
                "Step 1 (5 min): List the tasks you need to complete.",
                "Step 2 (15 min): Choose your most important task.",
                "Step 3 (25 min): Work on that task without distractions.",
                "Step 4 (5 min): Review your progress."
            ]
        ),
        "topic_guidance": topic_guidance
    }