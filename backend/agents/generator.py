def generator_agent(grade: int, topic: str, feedback=None):
    return {
        "explanation": f"This is a simple explanation of {topic} for grade {grade}.",
        "mcqs": [
            {
                "question": "What is an acute angle?",
                "options": ["Less than 90°", "Equal to 90°", "More than 90°", "None"],
                "answer": "Less than 90°"
            },
            {
                "question": "What is a right angle?",
                "options": ["90°", "45°", "180°", "60°"],
                "answer": "90°"
            }
        ]
    }