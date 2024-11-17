# Portuguese Monuments Information Retrieval System

This project aims to provide an efficient and user-friendly way to query data about Portuguese monuments using Apache Solr.

---

## Project Overview

This project utilizes Apache Solr to organize and retrieve data about Portuguese monuments. By leveraging Solr's advanced search capabilities, users can perform queries to obtain detailed information such as names, locations, architectural styles, and historical significance.



# Setup Instructions

## 1. Start Solr and Load Data

To set up the Solr environment and index the monument data:

1. **Navigate to the `m2/solr` directory:**
   ```bash
   cd m2/solr 
   ```

2. **Start Solr, configure the schema, and inde the data:**
    ```bash
    bash startup.sh
    ```
    - Starts a Solr container on `http://localhost:8983/solr`.

    - Configures the schema using ...

    - Indexes the monument data from `data.json`.


## 2. Run Queries

1. **Run the queries script:**
   ```bash
   bash query_with_curl.sh
   ```

    - Reads all `.json` query files from the `queries/` .

    - Executes each query using `curl` .

    - Saves the results in the `results/` directory (e.g., `query1_results.json`).


## Queries

### Query 1: Search for Churches in a Specific Location

**File**: `queries/query1.json`

```json
{
    "query": "(Nome:Igreja OR Tipo:igreja) AND Localizacao:Porto",
    "fields": "Nome, Localizacao, Tipo, Estatuto_Patrimonial",
    "params": {
        "defType": "edismax"
    }
}
```

- **Motivation** : Imagine walking through a city and coming across a beautiful church. You want to know more about it historical significance, architectural style, or whether it has any cultural heritage designation. This query addresses the need to find churches (Igreja) in a specific location (Porto).

