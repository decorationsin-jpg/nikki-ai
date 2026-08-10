"""
Nikki Universal Basic Knowledge & Q&A Engine.
Provides instant, accurate, friendly answers to all basic questions across science, geography,
math, general knowledge, history, everyday life, and identity.
"""
import re
import math
from typing import Optional

class BasicQAEngine:
    """
    Universal Knowledge Base & Q&A Engine for All Basic Questions.
    """

    def __init__(self):
        self.qa_database = {
            # Science & Nature
            "sky blue": "The sky is blue because Earth's atmosphere scatters sunlight in all directions, and blue light is scattered more than other colors because it travels as shorter, smaller waves (Rayleigh scattering).",
            "photosynthesis": "Photosynthesis is the process by which green plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar (glucose).",
            "gravity": "Gravity is a fundamental force of nature that pulls objects toward each other. Earth's gravity gives weight to objects and keeps our feet on the ground!",
            "rainbow": "A rainbow is formed when sunlight shines through raindrops in the atmosphere, bending (refracting) and reflecting light into a spectrum of 7 colors: Red, Orange, Yellow, Green, Blue, Indigo, and Violet.",
            "water formula": "Water is a chemical compound made of 2 hydrogen atoms and 1 oxygen atom, represented by the chemical formula **H2O**.",
            "black hole": "A black hole is a region in space where gravity is so strong that nothing, not even light, can escape from it. It forms when a massive star collapses at the end of its life.",

            # Geography & Capital Cities
            "capital of france": "The capital of France is **Paris**.",
            "capital of india": "The capital of India is **New Delhi**.",
            "capital of usa": "The capital of the United States is **Washington, D.C.**",
            "capital of japan": "The capital of Japan is **Tokyo**.",
            "largest ocean": "The largest and deepest ocean on Earth is the **Pacific Ocean**.",
            "how many continents": "There are **7 continents** on Earth: Asia, Africa, North America, South America, Antarctica, Europe, and Australia.",

            # Everyday Life & Technology
            "what is ai": "AI (Artificial Intelligence) refers to computer systems designed to perform tasks that typically require human intelligence, such as learning, reasoning, problem-solving, and voice interaction!",
            "how to learn coding": "Start with a friendly language like **Python**! Practice writing basic scripts every day, build small projects (like calculators or chatbots), and practice on platforms like LeetCode or GitHub.",
            "stay healthy": "Eat balanced meals with fresh fruits and vegetables, drink 2-3 liters of water daily, exercise for 30 minutes, get 7-8 hours of sleep, and reduce stress!",
            "who invented lightbulb": "Thomas Edison is credited with inventing the first commercially practical incandescent light bulb in 1879.",

            # Identity & Greetings
            "who are you": "I am Nikki (नक्की / निक्की), your 100% private, autonomous AI companion! I run locally on your device without any paid API keys.",
            "who created you": "I was built to be your 100% private, self-learning, emotion-aware local AI companion!",
            "what can you do": "I can run security audits (PIN 1805), execute commands, teach lessons, monitor IP cameras, speak in English/Hindi/Marathi, and solve math or coding problems!"
        }

    def answer_basic_question(self, query: str) -> Optional[str]:
        """Attempts to answer a basic question directly from internal knowledge or math evaluation."""
        q_lower = query.lower().strip()

        # Step 1: Check for basic Math expressions (e.g. 5+5, 12*4, 100/5)
        math_result = self._evaluate_math(q_lower)
        if math_result is not None:
            return f"🔢 **Math Answer**: `{query}` = **{math_result}**"

        # Step 2: Check Q&A Database keyword matches
        for key, answer in self.qa_database.items():
            if key in q_lower:
                return f"🌸 **Answer**: {answer}"

        return None

    def _evaluate_math(self, query: str) -> Optional[float]:
        """Evaluates basic math expressions safely (e.g. 2+2, 10*5, 100/4, 25-10)."""
        try:
            # Extract arithmetic expressions from query (e.g. "what is 2+2", "calculate 10*5")
            match = re.search(r'(\d+\.?\d*)\s*([\+\-\*/%])\s*(\d+\.?\d*)', query)
            if match:
                num1 = float(match.group(1))
                op = match.group(2)
                num2 = float(match.group(3))

                if op == '+': res = num1 + num2
                elif op == '-': res = num1 - num2
                elif op == '*': res = num1 * num2
                elif op == '/': res = num1 / num2 if num2 != 0 else None
                elif op == '%': res = num1 % num2
                else: res = None

                if res is not None:
                    # Return integer if whole number
                    return int(res) if res.is_integer() else round(res, 4)
        except Exception:
            pass
        return None
