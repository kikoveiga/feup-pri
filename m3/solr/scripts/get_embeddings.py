import sys, json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(text):
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == '__main__':
    data = json.load(sys.stdin)

    for document in data:
        title = document.get('title', '')
        objectives = document.get('objectives', '')
        learning_outcomes = document.get('learning_outcomes', '')
        combined_text = title + ' ' + objectives + ' ' + learning_outcomes
        document['vector'] = get_embeddings(combined_text)

    json.dump(data, sys.stdout, indent=4, ensure_ascii=False)