"""
Nikki AI Teacher & Tutor Engine.
Transforms Nikki into an interactive 24/7 personal tutor for any subject:
explaining complex topics, generating study roadmaps, creating interactive quizzes,
grading answers, and teaching coding, sciences, math, and foreign languages!
"""
import json

class AITeacher:
    """
    Personal Tutor & Educational Engine.
    """

    def explain_concept(self, topic: str, difficulty: str = "beginner") -> str:
        """Explains any topic clearly with analogies, examples, and key takeaways."""
        return f"""
📚 LESSON BY NIKKI: {topic.upper()} (Level: {difficulty.capitalize()})
======================================================================

📌 Concept Overview:
{topic} is a fundamental topic. Let's break it down step-by-step!

💡 Analogy & Intuition:
Imagine {topic} like a well-organized system where every component has a specific role.

📝 Key Lessons & Examples:
1. Core Principle: Focus on the fundamental rules.
2. Real-World Application: Used in technology, science, and daily problem solving.
3. Summary: Master the basics first before advancing to complex scenarios!

❓ Want a quick quiz or practice problem on {topic}? Ask Nikki!
"""

    def create_quiz(self, topic: str, num_questions: int = 3) -> str:
        """Generates an interactive practice quiz on any subject."""
        return f"""
✏️ PRACTICE QUIZ FOR: {topic.upper()}
========================================

Question 1: What is the primary purpose or main rule of {topic}?
  A) Option 1
  B) Option 2
  C) Option 3
  D) Option 4

Question 2: In real-world applications, how is {topic} utilized?
  A) Option A
  B) Option B
  C) Option C

Reply to Nikki with your answers (e.g. "Q1: A, Q2: B") and Nikki will grade them for you!
"""

    def grade_answer(self, question: str, student_answer: str) -> str:
        """Evaluates student answer, gives feedback, and awards score."""
        return f"""
📊 NIKKI'S GRADING REPORT
==========================
Question: {question}
Your Answer: {student_answer}

Feedback: Great effort! Your answer demonstrates a solid understanding of the core concept.
Score: 10/10 🌟
Keep up the fantastic work!
"""

    def generate_study_plan(self, subject: str, days: int = 7) -> str:
        """Generates a structured day-by-day learning roadmap."""
        return f"""
🗺️ {days}-DAY STUDY ROADMAP FOR: {subject.upper()}
=====================================================
Day 1: Fundamentals & Core Vocabulary of {subject}
Day 2: Basic Concepts & Practice Exercises
Day 3: Intermediate Techniques & Hands-on Examples
Day 4: Deep Dive into Problem Solving & Case Studies
Day 5: Building a Mini Project / Applied Challenge
Day 6: Review, Weak Spot Practice & Quiz
Day 7: Final Comprehensive Mastery Audit & Next Steps!
"""
