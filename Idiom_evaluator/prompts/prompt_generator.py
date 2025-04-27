class PromptGenerator:
    @staticmethod
    def generate_prompt(mode, **kwargs):
        """
        Генерирует универсальный промпт для всех типов задач
        :param mode: 'meaning', 'text' или 'literal'
        :param kwargs: аргументы для конкретного типа промпта
        :return: строка с промптом
        """
        base_instruction = """
        Инструкция: Внимательно прочитай задание и дай точный ответ в требуемом формате.
        Твой ответ должен содержать ТОЛЬКО номер правильного варианта в строгом формате:
        "Ответ: [номер]"
        Никаких дополнительных объяснений, обоснований или текста после ответа быть не должно.
        """
        
        if mode == 'meaning':
            return base_instruction + f"""
            Задание: Определи, какое значение соответствует данному выражению в тексте.
            Выражение: {kwargs['idiom']}
            Контекст: {kwargs['text']}
            Варианты ответа: {kwargs['responses']}
            Ответ:
            """
        elif mode == 'text':
            return base_instruction + f"""
            Задание: Определи, в каком тексте выражение означает указанное значение.
            Выражение: {kwargs['idiom']}
            Значение: {kwargs['current_meaning']}
            Тексты: {kwargs['texts']}
            Ответ:
            """
        elif mode == 'literal':
            return base_instruction + f"""
            Задание: Определи, используется ли выражение в прямом или переносном смысле.
            Выражение: {kwargs['idiom']}
            Контекст: {kwargs['text']}
            Варианты: 0 - буквальное значение, 1 - переносное значение
            Ответ:
            """
        else:
            raise ValueError(f"Unknown mode: {mode}")