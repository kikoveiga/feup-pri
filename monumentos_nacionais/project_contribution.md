
# Project Contribution Summary

## Data Collection

The dataset was sourced from **Wikipedia**, specifically from a page listing **National Monuments of Portugal by district**. This page contains links to separate pages for each district, where the individual monuments are listed. A total of **584 monuments** were scraped, covering all districts in Portugal. The monuments include a wide variety of structures, all classified as national monuments.

---

## Challenges and Data Curation

Several challenges were encountered during the data collection process. Although all the data was sourced from Wikipedia, the **HTML structure** of the pages was inconsistent across monuments. Key challenges included:

- **Varied HTML Structures**: There were two main types of infoboxes used on Wikipedia pages:
  - A **table-based infobox**.
  - An **infobox with nested tables**.
  This required different parsing methods to handle the diverse structures.

- **Inconsistent Paragraph Content**: While attempting to scrape the introductory paragraph for each monument as a description, it was found that some pages contained **empty paragraphs** or irrelevant content, such as **coordinates**, in the first paragraph.

- **Inconsistent Headers**: Similar information was sometimes labeled differently across monument pages. For example, the historical section for monuments could be titled either **“História”** or **“Historial”**, requiring adjustments in the scraping process to accommodate this variation.

To ensure a uniform dataset, several **data validation** and **cleaning** steps were applied:
- For each monument, if a required field was missing or could not be found, a default value such as **"Description not available"** was used. This helped maintain a consistent JSON structure across all records.
- All monument data was standardized to ensure that essential information like name, location, type, and description followed the same structure.

---

## Pipeline Description

### Tools and Techniques
The data was scraped using **BeautifulSoup** in Python, along with the **Requests** library to fetch HTML content from Wikipedia. Each monument’s information—including name, location, type, and description—was parsed from the HTML and stored in a structured format (JSON).

### Process Overview
The data collection process consisted of several key steps:
1. **Requesting Data**: HTTP requests were made to Wikipedia, and each request was validated using status code checks (200 indicating success).
2. **Parsing HTML**: The HTML content of each page was parsed to extract monument information, including handling different structures for infoboxes.
3. **Data Cleaning**: Uniformity was ensured across all records by filling in missing fields with placeholder values and ensuring consistency in field names.
4. **Saving Data**: The scraped data was saved in JSON format, with each monument represented as an individual JSON file containing its attributes.

---

## Dataset Characterization

The final dataset consists of **584 monuments** from all districts in Portugal. Each monument is described by a set of attributes, including:
- **Name**: The official name of the monument.
- **Location**: The district and city where the monument is located.
- **Type**: The type of monument (e.g., church, castle, etc.).
- **Description**: A brief description of the monument’s significance or history.
- **Historical Information**: Historical background (when available).
- **Coordinates**: Geographic coordinates (when available).

The data validation process ensured that all JSON entries followed a consistent structure, regardless of differences in the original HTML content. Challenges such as empty paragraphs, inconsistent headers, and varied infobox types were addressed by introducing default values and handling multiple structures in the scraping script.

---

## Information Needs and Querying

The envisioned search engine is designed to allow users to search for Portuguese national monuments based on various attributes, simulating real-world scenarios where users might encounter a monument and wish to retrieve information. The types of queries that the system is expected to handle include:

- **Color-based Queries**: For example, a user might search for **“blue church in Porto”**, and the search system should return relevant monuments matching the color and location criteria.
- **Type-based Queries**: Users may search for specific types of monuments, such as **“castles”** or **“churches”**.
- **Location-based Queries**: The search system should be able to retrieve monuments by location, such as **“monuments in Lisbon”** or **“monuments in Porto”**.

These information needs reflect the potential use cases of a tourist or researcher who may want to explore Portugal’s national heritage. The ability to search by **color**, **type**, and **location** enhances the system's usability, especially for travelers or users unfamiliar with specific monument names.
