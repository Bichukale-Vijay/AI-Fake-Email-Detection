# email_analyzer.py

import re
from collections import Counter

class EmailAnalyzer:
    """
    Standalone Email Analyzer Module
    (Not connected to main app — safe for future use)
    """

    def __init__(self, text):
        self.text = text
        self.cleaned = self._clean_text(text)

    def _clean_text(self, text):
        text = text.lower()
        text = re.sub(r'\W', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()

    def word_count(self):
        return len(self.cleaned.split())

    def char_count(self):
        return len(self.text)

    def find_urls(self):
        return re.findall(r"http[s]?://\S+|www\.\S+", self.text)

    def has_urls(self):
        return len(self.find_urls()) > 0

    def count_urls(self):
        return len(self.find_urls())

    def find_emails(self):
        return re.findall(r"\S+@\S+", self.text)

    def has_email(self):
        return len(self.find_emails()) > 0

    def contains_numbers(self):
        return any(char.isdigit() for char in self.text)

    def extract_keywords(self):
        keywords = [
            "urgent", "free", "winner", "click", "offer",
            "password", "bank", "verify", "account", "limited"
        ]
        return [word for word in keywords if word in self.cleaned]

    def keyword_count(self):
        return len(self.extract_keywords())

    def uppercase_ratio(self):
        if len(self.text) == 0:
            return 0
        upper = sum(1 for c in self.text if c.isupper())
        return upper / len(self.text)

    def digit_ratio(self):
        if len(self.text) == 0:
            return 0
        digits = sum(1 for c in self.text if c.isdigit())
        return digits / len(self.text)

    def special_characters(self):
        return re.findall(r"[!@#$%^&*(),.?\":{}|<>]", self.text)

    def has_urgent_tone(self):
        urgent_words = ["urgent", "asap", "immediately", "now"]
        return any(word in self.cleaned for word in urgent_words)

    def most_common_words(self, n=5):
        words = self.cleaned.split()
        return Counter(words).most_common(n)

    def summary(self):
        return {
            "word_count": self.word_count(),
            "char_count": self.char_count(),
            "urls": self.count_urls(),
            "emails": len(self.find_emails()),
            "keywords": self.extract_keywords(),
            "uppercase_ratio": self.uppercase_ratio(),
            "digit_ratio": self.digit_ratio(),
            "urgent": self.has_urgent_tone()
        }


# Optional test block (does NOT affect project)
if __name__ == "__main__":
    sample = "URGENT! Click here to verify your account: http://fake.com"
    analyzer = EmailAnalyzer(sample)
    print(analyzer.summary())