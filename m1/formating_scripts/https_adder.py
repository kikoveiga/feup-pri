import os
import json

def add_https_to_image_urls(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if "URL Imagem" in data and not data["URL Imagem"].startswith("https:"):
                data["URL Imagem"] = "https:" + data["URL Imagem"]
                
                with open(filepath, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
    
    print("Done!")

# Specify the directory containing the JSON files
directory_path = r"C:\Users\João Silva\Desktop\PRI\juntar_files\imoveis"
add_https_to_image_urls(directory_path)