import os
import json

def unify_json_files(input_folders, output_file):
    unified_data = []
    id_counter = 0

    for folder in input_folders:
        for child in os.listdir(folder):
            # Check if it is a dir
            if os.path.isdir(os.path.join(folder, child)):
                for filename in os.listdir(os.path.join(folder, child)):
                    if filename.endswith('.json'):
                        file_path = os.path.join(folder, child, filename)
                        #print(f"Processing file: {file_path}")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                id_counter += 1
                                data = {"id": id_counter, **data}
                                unified_data.append(data)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON in file {file_path}: {e}")
                            break
            
            # JSON file
            elif child.endswith('.json'):
                file_path = os.path.join(folder, child)
                #print(f"Processing file: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        id_counter += 1
                        data = {"id": id_counter, **data}
                        unified_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {file_path}: {e}")
                    break

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unified_data, f, ensure_ascii=False, indent=4)

    print("Done!")

if __name__ == "__main__":
    # NEED TO BE CHANGED ACORDINGLY TO THE MACHINE PATH TO THE FOLDERS
    input_folders = [r"C:\Users\João Silva\Desktop\PRI\juntar_files\districts",
                     r"C:\Users\João Silva\Desktop\PRI\juntar_files\imoveis",
                     r"C:\Users\João Silva\Desktop\PRI\juntar_files\rota_romanico_files"
                     ]
    output_file = r"C:\Users\João Silva\Desktop\PRI\juntar_files\combined_data.json"
    unify_json_files(input_folders, output_file)