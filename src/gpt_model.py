from abc import ABC, abstractmethod
import requests

class GPTModel(ABC):    
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate response from model
        
        Args:
            prompt: Text prompt for model
            
        Returns:
            Response from model
        """
        pass

class GeminiModel(GPTModel):
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        super().__init__(model_name)
        self.apikey = api_key

    def generate(self, prompt: str, proxies: dict = None) -> str:
        response = requests.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
            params={'key': self.apikey},
            headers={'Content-Type': 'application/json'},
            json={'contents': [{'parts': [{'text': prompt}]}]},
            proxies=proxies
        )
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

