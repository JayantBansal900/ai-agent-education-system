import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")


def generator_agent(grade: int, topic: str, feedback=None):
    try:
        prompt = f"""
        Create educational content for Grade {grade} on topic "{topic}".

        {f"Improve based on feedback: {feedback}" if feedback else ""}

        Return STRICT JSON:
        {{
          "explanation": "...",
          "mcqs": [
            {{
              "question": "...",
              "options": ["A", "B", "C", "D"],
              "answer": "A"
            }}
          ]
        }}
        """

        response = model.generate_content(prompt)

        text = response.text

        return json.loads(text)

    except Exception as e:
        return {
            "error": str(e),
            "raw_output": text if 'text' in locals() else None
        }