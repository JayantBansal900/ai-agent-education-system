def reviewer_agent(content: dict, grade: int):
    feedback = []

    explanation = content.get("explanation", "")
    mcqs = content.get("mcqs", [])

    # 🔹 Rule 1: Explanation length (age appropriate)
    if len(explanation.split()) > 100:
        feedback.append("Explanation is too long for the grade level")

    # 🔹 Rule 2: Simple language check
    difficult_words = ["approximately", "consequently", "furthermore"]
    for word in difficult_words:
        if word in explanation.lower():
            feedback.append(f"Word '{word}' is too complex for Grade {grade}")

    # 🔹 Rule 3: MCQ count
    if len(mcqs) < 2:
        feedback.append("Not enough MCQs")

    # 🔹 Rule 4: Check MCQ structure
    for i, mcq in enumerate(mcqs):
        if "question" not in mcq or "options" not in mcq or "answer" not in mcq:
            feedback.append(f"MCQ {i+1} is incomplete")

        if len(mcq.get("options", [])) != 4:
            feedback.append(f"MCQ {i+1} must have 4 options")

    # 🔹 Final decision
    status = "pass" if len(feedback) == 0 else "fail"

    return {
        "status": status,
        "feedback": feedback
    }