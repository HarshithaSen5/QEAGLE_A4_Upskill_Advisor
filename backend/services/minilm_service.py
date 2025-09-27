# minilm_service.py
"""
Fallback MiniLM or simple local model for text generation.
This can be a small transformer or a rule-based response.
"""
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

class MiniLMService:
    def _init_(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.generator = pipeline('text-classification', model=self.model, tokenizer=self.tokenizer)

    def generate(self, prompt, context=None):
        # Try to extract course names from the prompt for a friendly response
        import re
        courses_match = re.search(r"Recommended courses: (.+)", prompt)
        courses = []
        if courses_match:
            courses = [c.strip().title() for c in courses_match.group(1).split(",")]
        if courses:
            course_list = "\n".join([f"{i+1}. {c}" for i, c in enumerate(courses)])
            return (
                "Based on your current skills and your target role, I recommend the following courses to help you upskill:\n"
                f"{course_list}\n\nEach course is selected to address your missing skills and accelerate your learning journey. Good luck!"
            )
        else:
            return (
                "Based on your profile, I recommend a personalized set of courses to help you grow. Please check the list above for details!"
            )