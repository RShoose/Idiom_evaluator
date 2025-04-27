import json
import random

class DataLoader:
    @staticmethod
    def load_data(file_path):
        with open(file_path) as f:
            return json.load(f)
    
    @staticmethod
    def sample_data(data_dict, n_samples=50):
        if n_samples > len(data_dict):
            return data_dict
        sampled_keys = random.sample(list(data_dict), n_samples)
        return {k: data_dict[k] for k in sampled_keys}