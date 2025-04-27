import pandas as pd
from models.evaluator import ModelEvaluator
from prompts.prompt_generator import PromptGenerator
from utils.data_loader import DataLoader
from utils.result_handler import ResultHandler

class IdiomEvaluator:
    def __init__(self, model_provider="openrouter", model_name="deepseek"):
        self.evaluator = ModelEvaluator(model_provider, model_name)
        self.prompt_generator = PromptGenerator()
    
    def evaluate_tasks(self, data_dict, mode='meaning', n_samples=50):
        sampled_data = DataLoader.sample_data(data_dict, n_samples)
        
        df = pd.DataFrame(columns=['task_id', 'idiom', 'meaning', 'label', 'answer'])
        
        for i, info in sampled_data.items():
            idiom = info['idiom']
            current_meaning = info.get('current_meaning', '')
            label = info.get('correct_label', '')
            task_id = i
            
            try:
                if mode == 'meaning':
                    options = info['possible_meanings']
                    text = info['example']
                    prompt = self.prompt_generator.generate_prompt(mode, idiom=idiom, text=text, responses=options)
                
                elif mode == 'text':
                    texts = info['texts']
                    prompt = self.prompt_generator.generate_prompt(mode, idiom=idiom, current_meaning=current_meaning, texts=texts)
                
                elif mode == 'literal':
                    text = info['text']
                    prompt = self.prompt_generator.generate_prompt(mode, idiom=idiom, text=text)
                
                else:
                    raise ValueError(f"Unknown mode: {mode}")
                
                answer = self.evaluator.evaluate(prompt)
                df.loc[len(df)] = [task_id, idiom, current_meaning, label, answer]
            
            except Exception as e:
                print(f"Error processing task {task_id}: {str(e)}")
                continue
        
        return df

def main():
    # Инициализация
    evaluator = IdiomEvaluator(model_provider="openrouter", model_name="deepseek/deepseek-r1:free")
    
    # Загрузка данных
    data_loader = DataLoader()
    
    # Пример использования для literal.json
    literal_data = data_loader.load_data('literal.json')['task_1']
    literal_df = evaluator.evaluate_tasks(literal_data, mode='literal', n_samples=10)
    ResultHandler.evaluate_results(literal_df, binary=True)
    ResultHandler.save_results(literal_df, 'literal_results.jsonl')
    
    # Пример использования для three_meanings.json
    meanings_data = data_loader.load_data('three_meanings.json')
    meanings_df = evaluator.evaluate_tasks(meanings_data, mode='meaning', n_samples=10)
    ResultHandler.evaluate_results(meanings_df)
    ResultHandler.save_results(meanings_df, 'meanings_results.jsonl')
    
    # Пример использования для three_texts.json
    texts_data = data_loader.load_data('three_texts.json')
    texts_df = evaluator.evaluate_tasks(texts_data, mode='text', n_samples=10)
    ResultHandler.evaluate_results(texts_df)
    ResultHandler.save_results(texts_df, 'texts_results.jsonl')

if __name__ == "__main__":
    main()