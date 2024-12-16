import requests, os, json
from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()

    return "[" + ", ".join(map(str, embedding)) + "]"

def solr_knn_query(endpoint, core_name, embedding, top_k=30):
    url = f"{endpoint}/{core_name}/select"

    data = {
        "q": f"{{!knn f=vector topK={top_k}}}{embedding}",
        "fl": "id, Nome, Localizacao, Estilo, score",
        "rows": top_k,
        "wt": "json"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

def save_results_to_file(results, folder_path):
    output_file = os.path.join(folder_path, 'semantic_result.json')
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4, ensure_ascii=False)
    print(f"Results saved to {output_file}")

def main():
    QUERIES_FOLDER = "queries"
    SOLR_URL = "http://localhost:8983/solr"
    CORE_NAME = "monuments"

    queries = [
        {"folder": "queries/q1", "query": "Igreja Porto"},
        {"folder": "queries/q2", "query": "Barroco Porto"},
        {"folder": "queries/q3", "query": "Arquitetura gótica Lisboa património cultural"}
    ]

    for query_data in queries:
        folder_path = query_data["folder"]
        query_text = query_data["query"]

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        embedding = text_to_embedding(query_text)

        try:
            results = solr_knn_query(SOLR_URL, CORE_NAME, embedding)
            docs = results.get("response", {}).get("docs", [])

            save_results_to_file(docs, folder_path)

        except requests.HTTPError as e:
            print(f"Error querying for {query_text}: {e.response.text}")

if __name__ == '__main__':
    main()
