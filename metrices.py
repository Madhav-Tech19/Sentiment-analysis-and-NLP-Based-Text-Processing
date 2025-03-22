import os
import re
import nltk
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize

# Load stop words from folder
def load_stop_words(stop_words_folder):
    stop_words = set()
    for filename in os.listdir(stop_words_folder):
        if filename.endswith('.txt'):
            try:
                with open(os.path.join(stop_words_folder, filename), 'r', encoding='utf-8') as file:
                    stop_words.update([line.strip().lower() for line in file.readlines()])
            except UnicodeDecodeError:
                # Fallback to 'latin-1' encoding
                with open(os.path.join(stop_words_folder, filename), 'r', encoding='latin-1') as file:
                    stop_words.update([line.strip().lower() for line in file.readlines()])
    return stop_words

# Load master dictionary of positive and negative words
def load_master_dictionary(master_dict_folder):
    positive_words = set()
    negative_words = set()
    
    for filename in os.listdir(master_dict_folder):
        if filename.endswith('positive-words.txt'):
            try:
                with open(os.path.join(master_dict_folder, filename), 'r', encoding='utf-8') as file:
                    for line in file.readlines():
                        word = line.strip().lower()
                        if word and not word.startswith(';'): 
                            positive_words.add(word)
            except UnicodeDecodeError:
                with open(os.path.join(master_dict_folder, filename), 'r', encoding='latin-1') as file:
                    for line in file.readlines():
                        word = line.strip().lower()
                        if word and not word.startswith(';'):
                            positive_words.add(word)
        
        elif filename.endswith('negative-words.txt'):
            try:
                with open(os.path.join(master_dict_folder, filename), 'r', encoding='utf-8') as file:
                    for line in file.readlines():
                        word = line.strip().lower()
                        if word and not word.startswith(';'):
                            negative_words.add(word)
            except UnicodeDecodeError:
                with open(os.path.join(master_dict_folder, filename), 'r', encoding='latin-1') as file:
                    for line in file.readlines():
                        word = line.strip().lower()
                        if word and not word.startswith(';'):
                            negative_words.add(word)
    
    return positive_words, negative_words

# Helper functions
def count_syllables(word):
    vowels = "aeiou"
    word = word.lower() 
    count = 0
    prev_char = ""

    for char in word:
        if char in vowels and prev_char not in vowels:
            count += 1
        prev_char = char

    # Adjust for silent 'e' at the end
    if word.endswith("e"):
        count -= 1

    return max(1, count)

def is_complex_word(word):
    return count_syllables(word) >= 3

def count_personal_pronouns(text):
    pronouns = r'\b(I|we|my|ours|us)\b'
    return len(re.findall(pronouns, text, re.IGNORECASE))

def calculate_metrics(text, positive_words, negative_words):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    word_count = len(words)
    sentence_count = len(sentences)
    
    positive_score = sum(1 for word in words if word.lower() in positive_words)
    negative_score = sum(1 for word in words if word.lower() in negative_words)
    complex_word_count = sum(1 for word in words if is_complex_word(word))
    
    avg_sentence_length = word_count / sentence_count if sentence_count else 0
    percentage_complex_words = complex_word_count / word_count if word_count else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words * 100)
    syllables_per_word = sum(count_syllables(word) for word in words) / word_count if word_count else 0
    avg_word_length = sum(len(word) for word in words) / word_count if word_count else 0
    personal_pronouns = count_personal_pronouns(text)
    
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)
    
    return {
        "URL_ID": None, 
        "URL": None,
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVITY SCORE": subjectivity_score,
        "AVG SENTENCE LENGTH": avg_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words * 100,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_sentence_length,
        "COMPLEX WORD COUNT": complex_word_count,
        "WORD COUNT": word_count,
        "SYLLABLE PER WORD": syllables_per_word,
        "PERSONAL PRONOUNS": personal_pronouns,
        "AVG WORD LENGTH": avg_word_length
    }

def main():
    positive_words, negative_words = load_master_dictionary("MasterDictionary")
    stop_words = load_stop_words("StopWords")
    
    input_file = "Input.xlsx"
    output_file = "Output Data Structure.xlsx"
    
    df = pd.read_excel(input_file)
    results = []
    
    for _, row in df.iterrows():
        text_file = os.path.join('articles', f"{row['URL_ID']}.txt")
        try:
            with open(text_file, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"File not found: {text_file}. Skipping...")
            continue

        cleaned_text = " ".join(word for word in word_tokenize(text) if word.lower() not in stop_words)
        metrics = calculate_metrics(cleaned_text, positive_words, negative_words)
        metrics['URL_ID'] = row['URL_ID']
        metrics['URL'] = row['URL']
        results.append(metrics)

    columns_order = [
        "URL_ID", "URL", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE",
        "SUBJECTIVITY SCORE", "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS",
        "FOG INDEX", "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT",
        "WORD COUNT", "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"
    ]
    
    output_df = pd.DataFrame(results, columns=columns_order)
    output_df.to_excel(output_file, index=False)
    print("Data analysis completed. Results saved to:", output_file)

if __name__ == "__main__":
    main()
