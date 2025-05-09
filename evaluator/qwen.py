import requests
import time
from typing import Callable


class QwenAgent:
    def __init__(self,
                 system_prompt: str = None,
                 api_key: str = "sk-414d235f8c524df9995e46191072f7bf",     # 本地部署时可随意设置
                 url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                 model: str = "qwen-plus"):
        self.system_prompt = system_prompt
        self.api_key = api_key
        self.url = url
        self.model = model

    def call_qwen(self,
                  messages: list,
                  top_k: int = 20,
                  top_p: float = 0.8,
                  temperature: float = 0.7,
                  max_length: int = 2048):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_length,
            "top_k": top_k,
            "top_p": top_p,
            "temperature": temperature
        }

        attempt = 0
        max_attempts = 5
        wait_time = 1

        while attempt < max_attempts:
            try:
                response = requests.post(self.url, headers=headers, json=data)

                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                else:
                    print(f"Attempt {attempt + 1}: Failed with status {response.status_code}, retrying...")
            
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1}: Network error: {e}, retrying...")

            time.sleep(wait_time)
            attempt += 1

        raise Exception("Max attempts exceeded. Failed to get a successful response.")
    
    def basic_success_check(self, response):
        return bool(response and isinstance(response, str) and len(response.strip()) > 0)

    def run(self,
            prompt: str,
            top_k: int = 20,
            top_p: float = 0.8,
            temperature: float = 0.7,
            max_length: int = 2048,
            max_try: int = 5,
            success_check_fn: Callable = None):
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        success = False
        try_times = 0

        if success_check_fn is None:
            success_check_fn = self.basic_success_check

        while try_times < max_try:
            response = self.call_qwen(
                messages=messages,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                max_length=max_length,
            )

            if success_check_fn(response):
                success = True
                break
            else:
                try_times += 1
        
        return response, success
