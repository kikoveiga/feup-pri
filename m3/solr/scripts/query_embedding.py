import requests, os, json
from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()

    return "[" + ", ".join(map(str, embedding)) + "]"

def solr_knn_query(endpoint, core_name, embedding, top_k=10):
    url = f"{endpoint}/{core_name}/select"

    data = {
        "q": f"{{!knn f=vector topK={top_k}}}{embedding}",
        "fl": "id, Nome, Descricao, Lozalizacao, score",
        "rows": top_k,
        "wt": "json"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

def test_embedding_queries(queries_folder, solr_url, core_name):
    results = {}

    for query_folder in sorted(os.listdir(queries_folder)):
        folder_path = os.path.join(queries_folder, query_folder)

        if not os.path.isdir(folder_path):
            print(f"Skipping {query_folder}, not a folder.")
            continue

        query_file = os.path.join(folder_path, 'updated.json')
        print(query_file)
        result_path = os.path.join(folder_path, 'semantic_result.json')

        if not os.path.isfile(query_file):
            print (f"Skipping {query_folder}, updated.json not found.")
            continue

        with open(query_file, 'r', encoding='utf-8') as file:
            query_data = json.load(file)
            query_text = query_data.get('query', '')

        print(f"Generating embedding and testing query: {query_text} (Folder: {query_folder})")
        embedding = text_to_embedding(query_text)

        try:
            response = solr_knn_query(solr_url, core_name, embedding)
            results = response.get('response', {}).get('docs', [])
        except requests.HTTPError as e:
            print(f"Error {e.response.status_code}: {e.response.text}")
            results = []

        with open(result_path, 'w', encoding='utf-8') as file:
            print(f"Writing results to {result_path}")
            json.dump(results, file, indent=4, ensure_ascii=False)


def main():
    QUERIES_FOLDER = "queries"
    SOLR_URL = "http://localhost:8983/solr"
    CORE_NAME = "monuments"

    query_results = test_embedding_queries(QUERIES_FOLDER, SOLR_URL, CORE_NAME)

if __name__ == '__main__':
    main()
