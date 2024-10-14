import scrapy
import os
import re

import scrapy.exceptions

charTranslationTable = str.maketrans({
    "′": "'",
    "″": "''",
    "\"" : "",
    "\n": " ",
    "\u00A0": ", " # Non-breaking space
})

class Spider(scrapy.Spider):
    name = "wikipedia_spider"
    start_urls = [
        "https://pt.wikipedia.org/wiki/Categoria:Im%C3%B3veis_de_interesse_p%C3%BAblico_em_Portugal"
    ]

    def parse(self, response):
        #------------------------------------------------------------------------
        # Seguir os todos os links disponíveis, caso seja uma página de categoria
        # ----------------------------------------------------------------------- 
        if "Categoria" in response.url:
            categories = response.css("div.mw-category-group")
            links = []

            for category in categories:
                if category.css("h3::text").get().strip() != "":
                    links += category.css("a::attr(href)").getall() 

            for link in links:
                yield response.follow(link, self.parse) 

        #----------------------------------------
        # Scrapping da página caso seja um artigo
        #----------------------------------------
        else:
            # --------------------------------------
            # Título do artigo e criação do ficheiro
            # --------------------------------------
            titulo = response.css("h1.firstHeading span.mw-page-title-main::text").get()

            fileName = f"{titulo.lower().replace(" ", "_")}.json"

            file_path = os.path.join('filesv2', fileName)
            fd = open(file_path, "w", encoding="utf-8")
            
            fd.write("{\n" + f'"Nome": "{titulo}",\n')

            # -------------------------------
            # Escrever a descrição e história
            # -------------------------------
            conteudoSecao = ""
            counterParagrafos = 0

            for child in response.css("div.mw-content-ltr.mw-parser-output > *"):
                childTextContent = "".join(child.css("::text").getall()).strip()

                # Remover quaisquer referencias que possam existir no estilo [1]
                childTextContent = re.sub(r'\[.*?\]', '', childTextContent).strip()

                # Remover caracteres especiais
                childTextContent = childTextContent.translate(charTranslationTable)

                # Sair do loop quando chegar ao final da página
                if childTextContent in ["Referências", "Bibliografia", "Ver também", "Ligações externas", "Informações", "Galeria de imagens"]:
                    break

                if child.root.tag == "p":
                    conteudoSecao += childTextContent + " "
                    counterParagrafos += 1

                    if counterParagrafos == 1:
                        fd.write(f'"Descricao": "{conteudoSecao.strip()}",\n')
                        conteudoSecao = ""     
            
            # Caso não exista uma história
            if conteudoSecao == "":
                fd.write(f'"Historia": "Historia nao especificada",\n')
            else:
                fd.write(f'"Historia": "{conteudoSecao.strip()}",\n')

            #-------------------
            # Parse à infobox_v2
            #-------------------
            tableRows =  response.css(".infobox_v2 tr")
            tipo = ""
            estilo = ""
            estatuto = "Imovel de Interesse Publico"
            localização = ""
            coordenadas = ""

            for row in tableRows:
                header = "".join(row.css("th::text").getall()).strip().replace('\n', " ")

                if not header:
                    header = "".join(row.css("td:nth-child(1) *::text").getall()).replace('\n', " ").strip()
                    content = "".join(row.css("td:nth-child(2) *::text").getall()).strip().replace('\n', " ")
                else:   
                    content = "".join(row.css("td *::text").getall()).strip().replace('\n', " ") 

                if header == "Tipo":
                    tipo = content.translate(charTranslationTable)

                if header == "Estilo" or header == "Estilo(s)" or header == "Estilo dominante":   
                    estilo = content.translate(charTranslationTable)

                if header == "Localização":
                    localização = content.translate(charTranslationTable)

                if header == "Coordenadas":
                    coordenadas = content.translate(charTranslationTable)
            
            fd.write(f'"Tipo": "{tipo if tipo != "" else "Tipo nao especificado"}",\n')
            fd.write(f'"Estilo": "{estilo == "" and "Estilo nao especificado" or estilo}",\n')
            fd.write(f'"Estatuto Patrimonial": "{estatuto}",\n')
            fd.write(f'"Localizacao": "{localização if localização != "" else "Localizacao nao especificada"}",\n')

            #------------
            # Coordenadas
            #------------
            fd.write('"Coordenadas": ')

            if coordenadas == "":
                coordenadas = response.css("#coordinates::text").get()

            if coordenadas is not None:
                fd.write(f'"{coordenadas.translate(charTranslationTable)}",\n')
            else:
                fd.write('"Coordenadas nao especificadas",\n')

            #-------------------------------------------------
            # Procurar o link da primeira imagem na infobox_v2
            #-------------------------------------------------
            fd.write('"URL Imagem": ')

            linkImagem = response.css("#bodyContent img:first-of-type::attr(src)").get()

            if linkImagem is not None:
                fd.write(f'"{linkImagem}"\n')
            else:
                fd.write('"Imagem nao especificada"\n')

            fd.write("}")

            fd.close()

            self.log(f"Saved file {fileName}")