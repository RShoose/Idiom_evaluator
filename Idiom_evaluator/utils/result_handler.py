import re
from typing import Union

class AnswerProcessor:
    @staticmethod
    def extract_answer(raw_answer: str) -> Union[int, None]:
        """
        Универсальный метод извлечения ответа из текста модели
        Обрабатывает все форматы:
        - Ответ: 2
        - {"Ответ": "0"}
        - Просто число: 1
        - Ответ: Беспомощными (извлекает цифры из текста)
        """
        # Удаляем все кавычки и скобки
        cleaned = re.sub(r'[\"\'{}\[\]\(\)]', '', raw_answer.strip())
        
        # Ищем явное указание ответа
        explicit_match = re.search(
            r'(?:Ответ|ответ|Answer|answer|ans|ANS)[:\s]*(\d+)', 
            cleaned, 
            re.IGNORECASE
        )
        if explicit_match:
            return int(explicit_match.group(1))
        
        # Ищем просто число в тексте
        digit_match = re.search(r'\b(\d+)\b', cleaned)
        if digit_match:
            return int(digit_match.group(1))
        
        # Для бинарных ответов ищем 0/1 в любом месте
        binary_match = re.search(r'[^0-9]([01])(?![0-9])', cleaned)
        if binary_match:
            return int(binary_match.group(1))
        
        return None

    @staticmethod
    def process_task_answer(raw_answer: str, expected_type: type = int) -> Union[int, None]:
        """
        Обработка ответа с проверкой типа
        :param raw_answer: сырой ответ от модели
        :param expected_type: ожидаемый тип (int для номеров)
        :return: обработанный ответ или None если не удалось извлечь
        """
        answer = AnswerProcessor.extract_answer(raw_answer)
        return answer if isinstance(answer, expected_type) else None