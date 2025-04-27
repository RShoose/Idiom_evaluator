class Config:
    API_KEYS = {
        "openrouter": "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",
        "vsegpt": "sk-or-vv-88d08708d2efbc29012fcc7b33b43676e405019b439dcd37dffa995bd514cfd1"
    }
    
    MODELS = {
        "deepseek": "deepseek/deepseek-r1:free",
        "gpt4_nano": "openai/gpt-4.1-nano",
        "llama_maverick": "meta-llama/llama-4-maverick"
    }
    
    API_URLS = {
        "openrouter": "https://openrouter.ai/api/v1",
        "vsegpt": "https://api.vsegpt.ru/v1"
    }