import os

# Load Stop Words List
def load_stop_words(stop_words_folder):
    stop_words = set()
    for filename in os.listdir(stop_words_folder):
        if filename.endswith('.txt'):
            try:
                # open the file with 'utf-8' encoding
                with open(os.path.join(stop_words_folder, filename), 'r', encoding='utf-8') as file:
                    stop_words.update([line.strip().lower() for line in file.readlines()])
            except UnicodeDecodeError:
                # If UTF-8 fails, try 'latin-1' encoding
                with open(os.path.join(stop_words_folder, filename), 'r', encoding='latin-1') as file:
                    stop_words.update([line.strip().lower() for line in file.readlines()])
            except Exception as e:
                # Catch any other potential errors
                print(f"Error reading {filename}: {e}")
                
    return stop_words


#  Load Master Dictionary
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
                # Retry with 'latin-1' if utf-8 fails
                with open(os.path.join(master_dict_folder, filename), 'r', encoding='latin-1') as file:
                    for line in file.readlines():
                        word = line.strip().lower()
                        if word and not word.startswith(';'):
                            positive_words.add(word)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        
        elif filename.endswith('negative-words.txt'):
            try:
                with open(os.path.join(master_dict_folder, filename), 'r', encoding='utf-8') as file:
                    for line in file.readlines():
                        word = line.strip().lower()
                        if word and not word.startswith(';'): 
                            negative_words.add(word)
            except UnicodeDecodeError:
                # Retry with 'latin-1' if utf-8 fails
                with open(os.path.join(master_dict_folder, filename), 'r', encoding='latin-1') as file:
                    for line in file.readlines():
                        word = line.strip().lower()
                        if word and not word.startswith(';'):
                            negative_words.add(word)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return positive_words, negative_words


# Clean Text by Removing Stop Words
def clean_text(text, stop_words):
    words = text.split()
    cleaned_text = [word for word in words if word.lower() not in stop_words]
    return ' '.join(cleaned_text)

#  Filter Positive and Negative Words
def filter_positive_negative_words(positive_words, negative_words, stop_words):
    filtered_positive = [word for word in positive_words if word not in stop_words]
    filtered_negative = [word for word in negative_words if word not in stop_words]
    return set(filtered_positive), set(filtered_negative)


def main():
    stop_words_folder = 'StopWords'
    master_dict_folder = 'MasterDictionary'
    stop_words = load_stop_words(stop_words_folder)
    positive_words, negative_words = load_master_dictionary(master_dict_folder)
    
    print(f"Loaded {len(stop_words)} stop words.")
    print(f"Loaded {len(positive_words)} positive words.")
    print(f"Loaded {len(negative_words)} negative words.")
    filtered_positive, filtered_negative = filter_positive_negative_words(positive_words, negative_words, stop_words)
    print(f"Filtered positive words: {len(filtered_positive)}")
    print(f"Filtered negative words: {len(filtered_negative)}")
    
    with open('filtered_positive_words.txt', 'w', encoding='utf-8') as file:
        for word in filtered_positive:
            file.write(word + '\n')
    
    with open('filtered_negative_words.txt', 'w', encoding='utf-8') as file:
        for word in filtered_negative:
            file.write(word + '\n')
    
    print("Output files saved.")

if __name__ == "__main__":
    main()
