from openai import OpenAI
from ..config import Config
from ..utils import AnswerProcessor

class ModelEvaluator:
    def __init__(self, model_provider="openrouter", model_name="deepseek"):
        self.config = Config()
        self.model_provider = model_provider
        self.model_name = model_name
        self.client = self._initialize_client()
        
    def _initialize_client(self):
        if self.model_provider == "openrouter":
            return OpenAI(
                base_url=self.config.API_URLS["openrouter"],
                api_key=self.config.API_KEYS["openrouter"]
            )
        elif self.model_provider == "vsegpt":
            return OpenAI(
                api_key=self.config.API_KEYS["vsegpt"],
                base_url=self.config.API_URLS["vsegpt"]
            )
        else:
            raise ValueError(f"Unknown provider: {self.model_provider}")
    
    def evaluate(self, prompt, max_retries=3):

        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_tokens=10  # Ограничиваем длину ответа
                )
                
                raw_answer = completion.choices[0].message.content
                processed = AnswerProcessor.process_task_answer(raw_answer)
                
                if processed is not None:
                    return str(processed)  # Возвращаем строку для единообразия
                
                print(f"Не удалось извлечь ответ из: '{raw_answer}'. Попытка {attempt + 1}/{max_retries}")
                
            except Exception as e:
                print(f"Ошибка API: {str(e)}. Попытка {attempt + 1}/{max_retries}")
        
        return None  # После всех попыток