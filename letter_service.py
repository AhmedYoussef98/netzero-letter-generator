import requests
import json

class LetterService:
    def __init__(self, base_url="http://128.140.37.194:5000"):
        self.base_url = base_url
        
    def generate_letter(self, category, title, recipient, is_firstTime, prompt):
        """Generate a letter using the API"""
        url = f"{self.base_url}/generate-letter"
        
        payload = {
            "category": category,
            "title": title,
            "recipient": recipient,
            "is_firstTime": is_firstTime,
            "prompt": prompt
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to generate letter: {response.text}"}
    
    def save_letter(self, letter, letter_type, recipient, subject, is_first_comm):
        """Save the letter using the API"""
        url = f"{self.base_url}/save-letter"
        
        payload = {
            "letter": letter,
            "letter_type": letter_type,
            "recipient": recipient,
            "subject": subject,
            "is_first_comm": is_first_comm
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to save letter: {response.text}"}
