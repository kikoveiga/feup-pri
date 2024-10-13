import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as GeckoService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import json
import re

class RotaRomanicoScraper:
    def __init__(self):
        options = Options()
        # Uncomment the line below to run Firefox in headless mode (no GUI)
        # options.headless = True
        self.driver = webdriver.Firefox(service=GeckoService(GeckoDriverManager().install()), options=options)

    def scrape(self):
        start_url = "https://www.rotadoromanico.com/pt/monumentos/"
        self.driver.get(start_url)
        
        # Allow time for the page to fully load
        time.sleep(5)
        
        # Extract monument links from the main page
        monument_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.col-sm-6.col-md-4.col-lg-4.col-xl-3.p-0.monument-bg")
        print("Monument Divs Found:", len(monument_divs))

        # Get links for all monuments
        links = [div.find_element(By.TAG_NAME, 'a').get_attribute('href') for div in monument_divs]

        for link in links:
            self.parse_monument(link)
            # Go back to the main page after scraping
            self.driver.get(start_url)
            time.sleep(5)  # Wait for the page to load again
        
        # Close the driver after scraping
        self.driver.quit()

    def parse_monument(self, link):
        # Navigate to the monument page
        self.driver.get(link)

        # Allow time for the page to fully load
        time.sleep(5)
        
        ############
        ### Name ###
        ############
        monument_name = self.driver.find_element(By.TAG_NAME, 'h2').text.strip()

        monument_data = {
            'Nome': monument_name,
        }

        ################
        ### Location ###
        ################
        monument_location = self.driver.find_element(By.CSS_SELECTOR, 'div.info p:nth-of-type(3)').text.strip()

        ###################
        ### Coordenadas ###
        ###################
        monument_coordenates = self.driver.find_element(By.CSS_SELECTOR, 'div.info p:nth-of-type(2)').text.strip()

        ###############
        ### History ###
        ###############
        paragraphs = self.driver.find_elements(By.CSS_SELECTOR, 'div.rich-text')
        monument_description = " ".join([p.text.strip() for p in paragraphs])
        monument_description = monument_description.replace('\n', ' ').strip()
        monument_description = ' '.join(monument_description.split())

        monument_data['Historia'] = monument_description


        additional_paragraphs = self.driver.find_elements(By.CSS_SELECTOR, 'div.info > div.rich-text')
        additional_description = " ".join([p.text.strip() for p in additional_paragraphs])
        additional_description = additional_description.replace('\n', ' ').strip()
        additional_description = ' '.join(additional_description.split())

        monument_data['Descricao'] = additional_description

        #############
        ### Image ###
        #############
        image_div = self.driver.find_element(By.CSS_SELECTOR, 'div.slick-active div.highlight-background.item')
        style_attr = image_div.get_attribute('style')
        image_url_match = re.search(r'url\("(.+?)"\)', style_attr)
        if image_url_match:
            image_url = image_url_match.group(1)
            if image_url.startswith('/'):
                image_url = f"https://www.rotadoromanico.com{image_url}"
        else:
            image_url = None


        ###############################
        ### Tipologia/Classificação ###
        ###############################
        monument_paragraphs = self.driver.find_elements(By.CSS_SELECTOR, 'div.info-monument.pt-3 p')

        for monument_paragraph in monument_paragraphs:
            category_titles = monument_paragraph.find_elements(By.CSS_SELECTOR, 'span.category-title')
            if category_titles:
                monument_info = category_titles[0].text.strip()
                if monument_info == "Tipologia:":
                    monument_data["Tipo"] = monument_paragraph.find_element(By.CSS_SELECTOR, 'span:nth-of-type(2)').text.strip()
                    monument_data["Estilo"] = "Românico"

                if monument_info == "Classificação:":
                    if "Tipo" in monument_data:
                        monument_data["Estatuto Patrimonial"] = monument_paragraph.find_element(By.CSS_SELECTOR, 'span:nth-of-type(2)').text.strip()
                    else:
                        monument_data["Tipo"] = "Tipo não especificado"
                        monument_data["Estilo"] = "Românico"
                        monument_data["Estatuto Patrimonial"] = monument_paragraph.find_element(By.CSS_SELECTOR, 'span:nth-of-type(2)').text.strip()

        if "Tipo" not in monument_data and "Estatuto Patrimonial" not in monument_data:
            monument_data["Tipo"] = "Tipo não especificado"
            monument_data["Estilo"] = "Românico"
            monument_data["Estatuto Patrimonial"] = "Estatuto patrimonial não especificado"
            
        elif "Estatuto Patrimonial" not in monument_data:
            monument_data["Estatuto Patrimonial"] = "Estatuto patrimonial não especificado"

        monument_data["Localizacao"] = monument_location
        monument_data["Coordenadas"] = monument_coordenates
        monument_data["URL Imagem"] = image_url

        filename = os.path.join("rota_romanico_files", f"{monument_name}.json")
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(monument_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scraper = RotaRomanicoScraper()
    scraper.scrape()