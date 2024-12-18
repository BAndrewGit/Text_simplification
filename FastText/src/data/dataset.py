import json
from sklearn.model_selection import train_test_split

def load_dataset(file_path, test_size=0.2, random_state=42):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
    return train_data, test_data