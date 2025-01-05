import pandas as pd
import re
from pathlib import Path

def load_dataset(file_path):
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Dataset not found at {file_path}")
    return pd.read_csv(file_path)

def extract_words_from_dataset(dataset):
    all_words = []
    for text in dataset['text']:
        words = extract_words_from_text(text)
        all_words.extend(words)
    return all_words

def save_words_to_file(words, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for word in words:
            file.write(word + '\n')

def extract_words_from_text(text):
    text = re.sub(r'[0-9.,]', '', text)  
    text = re.sub(r'[^஀-௿\s]', '', text)  
    words = text.split()  
    return words



if __name__ == "__main__":

    dataset_path = r"/Users/divyanicassionprinston/Desktop/AI_project/dataset.csv" 
    output_file = r"/Users/divyanicassionprinston/Desktop/AI_project/WordList.txt" 

    print("Loading dataset...")
    dataset = load_dataset(dataset_path)

    print("Extracting words...")
    extracted_words = extract_words_from_dataset(dataset)

    print(f"Saving words to {output_file}...")
    save_words_to_file(extracted_words, output_file)

    print(f"Extracted {len(extracted_words)} words successfully!")
