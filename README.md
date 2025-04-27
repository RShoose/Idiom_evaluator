# Idiom_evaluator
Пример использования
```
evaluator = ModelEvaluator()
prompt_gen = PromptGenerator()
answer_processor = AnswerProcessor()

# генерация промпта
prompt = prompt_gen.generate_prompt(
    mode='meaning',
    idiom="бить баклуши",
    text="Он целыми днями бил баклуши вместо работы",
    responses=["1 - работать", "2 - бездельничать", "3 - ругаться"]
)

# получение ответа
raw_answer = evaluator.evaluate(prompt)  # Может вернуть "Ответ: 2" или другой формат

# обработка
answer = answer_processor.process_task_answer(raw_answer)
print(answer)
```
