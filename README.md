# FEUP-PRI

&nbsp;&nbsp;&nbsp;&nbsp;This project explores the application of Information Processing and Retrieval techniques to the study of Portuguese monuments. We
aim to develop an efficient system for collecting, organizing, and
retrieving relevant data about historical landmarks across Portugal.
This work contributes to the digital preservation of cultural heritage
and supports the creation of user-friendly tools for educational and
touristic purposes.

## Milestone #1 - Data Preparation

&nbsp;&nbsp;&nbsp;&nbsp;The first milestone of this project focuses on data collection and processing. For the collection of data, we first determined what websites we would take the information from. We selected two different sources with three specific links: [**Rota do Românico**](https://www.rotadoromanico.com/en/Monuments/); [**Wikipedia - List of National Monuments**](https://en.wikipedia.org/wiki/List_of_national_monuments_of_Portugal); [**Wikipedia - Categoria: Imóveis de interesse público em Portugal**](https://pt.wikipedia.org/wiki/Categoria:Im%C3%B3veis_de_interesse_p%C3%BAblico_em_Portugal).

### How the code works

&nbsp;&nbsp;&nbsp;&nbsp;As we explored the websites, we found that each one had a different HTML structure and, in some cases, even the same website had different HTML structures for each monument. To address this, we developed three distinct web scrapers: one for [**Rota do Românico**](./rota_do_romanico/project_contribution.md); one for [**Wikipedia - List of National Monuments**](./monumentos_nacionais/project_contribution.md); and one for [Wikipedia - List of Public Interest Real Estate](./imoveis_interesse_publico/). Each link provides a detailed explanation of how the data collection process and pipeline were implemented for each source.

