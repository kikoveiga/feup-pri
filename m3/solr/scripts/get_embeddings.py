import sys, json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(text):
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == '__main__':
    data = json.load(sys.stdin)

    for document in data:
        nome = document.get("Nome", "")
        descricao = document.get("Descricao", "")
        historia = document.get("Historia", "")
        tipo = document.get("Tipo", "")
        estilo = document.get("Estilo", "")
        estatuto_patrimonial = document.get("Estatuto Patrimonial", "")
        localizacao = document.get("Localizacao", "")

        combined_text = " ".join(filter(None, [nome, descricao, historia, tipo, estilo, estatuto_patrimonial, localizacao]))

        if combined_text:
            document['vector'] = get_embeddings(combined_text)
        else:
            document['vector'] = []

    json.dump(data, sys.stdout, indent=4, ensure_ascii=False)