import json
import re
from nltk.corpus import wordnet as wn
import nltk
import requests

# Download WordNet if not already downloaded
nltk.download("wordnet")
nltk.download("omw-1.4")

# Configuration
DATA_FILE = "solr/data.json"  # Input JSON file
SYNONYMS_FILE = "synonyms.txt"  # Output file for Solr synonyms
FIELDS_TO_PROCESS = ["Nome", "Descricao", "Historia", "Localizacao"]  # Fields to process
LANG = "por"  # Language code for Portuguese


# Step 1: Extract Unique Words from Specified Fields
def extract_unique_words(data_file, fields):
    unique_words = set()
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        for field in fields:
            if field in item and isinstance(item[field], str):
                words = tokenize_text(item[field])
                unique_words.update(words)

    return unique_words


def tokenize_text(text):
    # Tokenize text into words, remove punctuation, and convert to lowercase
    return re.findall(r'\b\w+\b', text.lower())


# Step 2: Generate Synonyms Using WordNet
def get_synonyms_from_wordnet(word, lang=LANG):
    synonyms = set()
    for synset in wn.synsets(word, lang=lang):
        for lemma in synset.lemmas(lang):
            synonyms.add(lemma.name())
    return synonyms


# Optional: Step 2 Alternative - Generate Synonyms Using an API
def get_synonyms_from_api(word):
    url = f"https://api.openthesaurus.pt/v1/synonyms/{word}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [syn['term'] for syn in data.get('synonyms', [])]
    except requests.exceptions.RequestException:
        pass
    return []


# Step 3: Generate Synonyms for All Unique Words
def generate_synonyms(unique_words, method="wordnet"):
    synonym_dict = {}
    for word in sorted(unique_words):
        if method == "wordnet":
            synonyms = get_synonyms_from_wordnet(word)
        elif method == "api":
            synonyms = get_synonyms_from_api(word)
        else:
            raise ValueError("Invalid method for generating synonyms. Use 'wordnet' or 'api'.")

        if synonyms:
            synonym_dict[word] = synonyms
    return synonym_dict


# Step 4: Save Synonyms to Solr-Compatible Format
def save_synonyms_to_file(synonym_dict, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for word, synonyms in synonym_dict.items():
            f.write(f"{word}, {', '.join(synonyms)}\n")


# Main Execution
if __name__ == "__main__":
    print("Extracting unique words...")
    unique_words = extract_unique_words(DATA_FILE, FIELDS_TO_PROCESS)
    print(f"Found {len(unique_words)} unique words.")

    print("Generating synonyms...")
    # Change method to "api" if you want to use the API instead
    synonyms = generate_synonyms(unique_words, method="wordnet")
    print(f"Generated synonyms for {len(synonyms)} words.")

    print("Saving synonyms to file...")
    save_synonyms_to_file(synonyms, SYNONYMS_FILE)
    print(f"Synonyms saved to {SYNONYMS_FILE}.")
