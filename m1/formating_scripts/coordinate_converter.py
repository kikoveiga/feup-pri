import json
import re

def convert_coordinates(coord_str):
    pattern = r'(\d+).(\d+), -?(\d+).(\d+)'
    match = re.match(pattern, coord_str)

    if match:
        return

    # Regular expression to extract degrees, minutes, and seconds
    pattern = r'(\d+)(?:\°|\º)\s*(\d+)′\s*(?:(\d+)(?:[,.](\d+))?(?:\″|\"|)?)?\s*([NS]),?\s*(\d+)(?:\°|\º)\s*(\d+)′\s*(?:(\d+)(?:[,.](\d+))?(?:\″|\")?\s*)?([EO])'
    match = re.match(pattern, coord_str)
    
    if not match:
        pattern = r'(\d+)(?:\°|\º)\s*(\d+)\'\s*(?:(\d+)(?:[,.](\d+))?(?:\'\'|\")?\s*)?([NS]),?\s*(\d+)(?:\°|\º)\s*(\d+)\'\s*(?:(\d+)(?:[,.](\d+))?(?:\'\'|\")?\s*)?([EO])'
        match = re.match(pattern, coord_str)
    
    if not match:
        print("Could not match coordinates:", coord_str)
        return coord_str
    
    lat_deg, lat_min, lat_sec, lat_frac, lat_dir, lon_deg, lon_min, lon_sec, lon_frac, lon_dir = match.groups()

    #Print all the groups
    #print(lat_deg, lat_min, lat_sec, lat_frac, lat_dir, lon_deg, lon_min, lon_sec, lon_frac, lon_dir)
    
    # Convert to decimal degrees
    lat = int(lat_deg) + int(lat_min or 0) / 60 + (int(lat_sec or 0) + (int(lat_frac or 0) / 10**len(lat_frac) if lat_frac else 0)) / 3600
    lon = int(lon_deg) + int(lon_min or 0) / 60 + (int(lon_sec or 0) + (int(lon_frac or 0) / 10**len(lon_frac) if lon_frac else 0)) / 3600
    
    if lat_dir == 'S':
        lat = -lat
    if lon_dir == 'O':
        lon = -lon
    
    return f"{lat:.6f}, {lon:.6f}"


def main():
    with open('combined_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for item in data:
        # Converter coordenadas
        if "Coordenadas" in item:
            if item["Coordenadas"] == "Coordenadas indisponíveis":
                continue

            if item["Coordenadas"] == "Coordenadas indisponiveis" or item["Coordenadas"] == "Cordenadas indisponiveis":
                item["Coordenadas"] = "Coordenadas indisponíveis"
                continue
            
            # Check to see if the coordinartes are already in decimal format
            if re.match(r'^-?\d+,\d+, -?\d+,\d+$', item["Coordenadas"]):
                #print("Coordinates already in decimal format for id:", item["id"])
                item["Coordenadas"] = item["Coordenadas"].replace(",", ".")
                continue
            else:
                #print("Converting coordinates for id:", item["id"], " New Value:", convert_coordinates(item["Coordenadas"]))
                item["Coordenadas"] = convert_coordinates(item["Coordenadas"])

        if "Historia" in item:
            if item["Historia"] == "Histório Indispoinível":
                print("Correcting history...")
                item["Historia"] = "História indisponível"

        if "Tipo" in item:
            if item["Tipo"] == "Tipo Desconhecido":
                print("Correcting type...")
                item["Tipo"] = "Tipo indisponível"

            # Remove things inside () and [] if they are present
            item["Tipo"] = re.sub(r'\(.*\)', '', item["Tipo"])

            

    with open('converted_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Done!")

if __name__ == "__main__":
    main()