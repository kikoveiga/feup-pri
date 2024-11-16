import os
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import re

# Scrape district links from the main page
def scrape_district_links(main_url):
    response = requests.get(main_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        district_links = []
        for category_group in soup.find_all('div', class_='mw-category-group'):
            for a_tag in category_group.find_all('a', href=True):
                full_url = "https://pt.wikipedia.org" + a_tag['href']
                district_links.append(full_url)
        return district_links
    else:
        print(f"Failed to retrieve the main page. Status code: {response.status_code}")
        return []

# Scrape monument links from a district page
def scrape_monument_links(district_url, scrape_subcategories=True):
    response = requests.get(district_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        monument_links = []
        
        # First, scrape monuments directly from the district page
        for category_group in soup.find_all('div', class_='mw-category-group'):
            for a_tag in category_group.find_all('a', href=True):
                full_url = "https://pt.wikipedia.org" + a_tag['href']
                monument_links.append(full_url)
        
        # If allowed, check for subcategories and follow the links to scrape their monuments
        if scrape_subcategories:
            subcategory_section = soup.find('div', id='mw-subcategories')
            if subcategory_section:
                for subcategory in subcategory_section.find_all('a', href=True):
                    subcategory_url = "https://pt.wikipedia.org" + subcategory['href']
                    # Scrape monument links from the subcategory page, but don't scrape further subcategories
                    monument_links.extend(scrape_monument_links(subcategory_url, scrape_subcategories=False))
        
        return monument_links
    else:
        print(f"Failed to retrieve {district_url}. Status code: {response.status_code}")
        return []
    
# Helper function to convert DMS to decimal
def dms_to_decimal(coord_string):
    match = re.match(r"(\d+)° (\d+)′ (\d+)″ ([NSEO])", coord_string)
    if not match:
        return None

    degrees, minutes, seconds, direction = match.groups()
    decimal = int(degrees) + int(minutes) / 60 + int(seconds) / 3600

    # Convert to negative for south or west
    if direction in ['S', 'O']:
        decimal = -decimal

    return round(decimal, 6)


# Scrape monument details from a monument page
def scrape_monument_details(monument_url):
    response = requests.get(monument_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        monument_data = {}

        # Default values for the monument data
        monument_data['Nome'] = "Sem Nome"
        monument_data['Descricao'] = "Descrição Indisponível"
        monument_data['Historia'] = "Histório Indisponível"
        monument_data['Tipo'] = "Tipo Desconhecido"
        monument_data['Estilo'] = "Estilo não especificado"
        monument_data['Estatuto Patrimonial'] = "Monumento Nacional"
        monument_data['Localizacao'] = "Localizaçao desconhecida"
        monument_data['Coordenadas'] = "Cordenadas indisponiveis"
        monument_data['URL Imagem'] = "Sem imagem disponível"

        monument_name = soup.find('h1')
        if monument_name:
            monument_data['Nome'] = monument_name.get_text().strip()

        # Two types of infoboxes 
        # Table based infobox 
        infobox_table = soup.find('table', class_='infobox')
        if infobox_table:
            rows = infobox_table.find_all('tr')
            for row in rows:
                header = row.find("td", {"scope": "row"})  # Correct selector for table-based infobox
                value = row.find("td", {"style": "vertical-align: top; text-align: left;"})
                if header and value:
                    header_text = header.get_text().strip()
                    value_text = ' '.join(value.stripped_strings).strip()  # Handle nested tags
                    
                    # Match header and assign values
                    if "Localização" in header_text or "Cidade" in header_text:
                        monument_data['Localizacao'] = value_text
                    if "Tipo" in header_text:
                        monument_data['Tipo'] = value_text
                    if "Estilo" in header_text:
                        monument_data['Estilo'] = value_text
                    if "Coordenadas" in header_text:
                        # Attempt to parse and convert coordinates
                        coordinate_parts = re.findall(r"(\d+° \d+′ \d+″ [NSEO])", value_text)
                        if len(coordinate_parts) == 2:  # Expecting two parts: latitude and longitude
                            lat = dms_to_decimal(coordinate_parts[0])
                            lon = dms_to_decimal(coordinate_parts[1])
                            if lat is not None and lon is not None:
                                monument_data['Coordenadas'] = f"{lat}, {lon}"

        # Infobox with nexted tables
        infobox_div = soup.find('div', class_='infobox_v2')
        if infobox_div:
            # Extract tables within the div-based infobox
            nested_tables = infobox_div.find_all('table')
            for table in nested_tables:
                rows = table.find_all('tr')
                for row in rows:
                    header = row.find("th")  
                    value = row.find("td")
                    if header and value:
                        header_text = header.get_text().strip()
                        value_text = ' '.join(value.stripped_strings).strip() 
                        
                        if "Localização" in header_text or "Cidade" in header_text:
                            monument_data['Localizacao'] = value_text
                        if "Tipo" in header_text:
                            monument_data['Tipo'] = value_text
                        if "Estilo" in header_text:
                            monument_data['Estilo'] = value_text
                        if "Coordenadas" in header_text:
                            # Attempt to parse and convert coordinates
                            coordinate_parts = re.findall(r"(\d+° \d+′ \d+″ [NSEO])", value_text)
                            if len(coordinate_parts) == 2:  # Expecting two parts: latitude and longitude
                                lat = dms_to_decimal(coordinate_parts[0])
                                lon = dms_to_decimal(coordinate_parts[1])
                                if lat is not None and lon is not None:
                                    monument_data['Coordenadas'] = f"{lat}, {lon}"

        # Get description
        description = ""
        for p_tag in soup.find_all('p'):
            # Skip paragraphs with no important content  like cordinates 
            if p_tag.find_parent(id="coordinates") or p_tag.find_parent(id="mw-indicator-coordinates"):
                continue
            
            # Skip empty paragraphs 
            if not p_tag.get_text().strip():
                continue

            # Skip paragraphs with no important content
            if 'noprint' in p_tag.get('class', []) or 'navbar' in p_tag.get('class', []):
                continue
            
            description_text = re.sub(r'\[\d+\]', '', p_tag.get_text().strip())  # Remove [n] references
            description += description_text + "\n"


        monument_data['Descricao'] = description.strip()

        # Get historical info
        history_section = soup.find('h2', {'id': 'História'}) or soup.find('h2', {'id': 'Historial'})
        if history_section:
            history_content = history_section.find_next('p')
            if history_content:
                monument_data['Historia'] = re.sub(r'\[\d+\]', '', history_content.get_text().strip())  # Remove [n] references




        # Save URL of monument image  
        image_tag = infobox_table.find('img') if infobox_table else (infobox_div.find('img') if infobox_div else None)
        if image_tag and 'src' in image_tag.attrs:
            monument_data['URL Imagem'] = "https:" + image_tag['src'] 

        return monument_data
    else:
        print(f"Failed to retrieve monument page: {monument_url}. Status code: {response.status_code}")
        return {}


# Save the monument data to a JSON 
def save_monument_data(district_name, monument_data):
    # Code for accents and more
    district_name = urllib.parse.unquote(district_name).replace('_', ' ').replace(':', '').strip()

    # Create a folder disctrict if dont exist
    base_dir = os.path.join('monumentos_nacionais', 'districts')
    folder_path = os.path.join(base_dir, district_name)
    os.makedirs(folder_path, exist_ok=True)

    # Create a valid JSON filename
    filename = monument_data['Nome'].replace(' ', '_').replace('/', '_').replace(':', '_') + '.json'
    file_path = os.path.join(folder_path, filename)

    # Save monument to JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(monument_data, f, indent=4, ensure_ascii=False)



def main():
    # Scrape all district links from the main page
    main_url = "https://pt.wikipedia.org/wiki/Categoria:Monumentos_nacionais_em_Portugal_por_distrito"
    district_links = scrape_district_links(main_url)
    count = 0

    # For each district, scrape the monument links
    for district_url in district_links:
        district_name = district_url.split('_')[-1]  # Get district name from URL
        monument_links = scrape_monument_links(district_url)

        # For each monument, scrape the details and save them
        for monument_url in monument_links:
            count += 1
            monument_data = scrape_monument_details(monument_url)
            if monument_data:
                save_monument_data(district_name, monument_data)
        
        print(f"All monuments for district {district_name} have been scraped and saved.")

    print(f"Scrapped monument stotla is {count} ")

if __name__ == "__main__":
    main()
