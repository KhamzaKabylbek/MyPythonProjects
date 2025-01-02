import aiohttp
import asyncio
import json
from typing import Dict, Any, Optional

class GeminiClient:
    def __init__(self, api_key: str = "AIzaSyACoYC9FFJMPirwxQV85iKzAyJozjOWXyM"):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-1.5-flash"
    
    async def generate_content(self, prompt: str) -> Optional[str]:
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
                    if response.status == 200 and "candidates" in data:
                        return data["candidates"][0]["content"]["parts"][0]["text"]
                    return None
        except Exception as e:
            print(f"Ошибка: {e}")
            return None

async def main():
    client = GeminiClient()
    
    while True:
        prompt = input("Введите запрос (или 'выход' для завершения): ")
        if prompt.lower() == "выход":
            break
            
        response = await client.generate_content(prompt)
        if response:
            print(f"\nОтвет: {response}\n")
        else:
            print("\nНе удалось получить ответ\n")

if __name__ == "__main__":
    asyncio.run(main())