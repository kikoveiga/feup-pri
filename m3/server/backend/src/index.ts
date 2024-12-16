import express, { Express, Request, Response } from "express";
import dotenv from "dotenv";
import { execFile } from "child_process";
import path from "path";
import cors from "cors";

dotenv.config();

const app: Express = express();

// Middleware for JSON parsing
app.use(express.json());

const port = process.env.PORT || 3000;

const solrUrl = "http://localhost:8983/solr/monuments/select";
const scriptPath = path.resolve(__dirname, "solr_query_script.sh");

// Use cors
app.use(cors());

app.get("/", (req: Request, res: Response) => {
  res.send("Hmmmm, there's nothing here to be seen");
});

/**
 * Route to apply a specific query to SOLR, using the search bar
 * 'query' must be an element present in the req body. If not present, the request will be ignored
 * 'number' must be an element present in the req body, indicating the number of answers to return (-1 for all). If not present, the request will be ignored
 * 
 * Returns only the name and image URL for every monument found
 */
app.post("/query", (req: any, res: any) => {
  if (!req.body){
    return res.status(400).send("400 - No body found in the request");
  }

  const { query, number } = req.body;

  if (!query) {
    return res.status(400).json({error: "400 - No query was provided in the body request"});
  }

  if (!number) {
    return res.status(400).json({error: "400 - No number was provided in the body request"});
  }

  const queryJson = JSON.stringify({
    "query": query.toString(),
    "params": {
      "defType": "edismax",
      "qf": "Nome Descricao Historia Tipo Estilo Localizacao",
      "fl": "id, Nome, Localizacao",
      "q.op": "OR",
      "rows": 20
    }
  });

  execFile(scriptPath, [solrUrl, queryJson], (error, stdout, stderr) => {
    if (error) {
      console.error("Error executing shell script:", error);
      return res.status(500).json({ error: "500 - Internal Server Error executing shell script" });
    }

    if (stderr) {
      console.error("Shell script error:", stderr);
      return res.status(500).json({ error: "500 - Internal Server Error in the shell script: " + error});
    }

    try {
      const jsonResponse = JSON.parse(stdout);

      console.log(jsonResponse.response.docs);

      return res.status(200).json(jsonResponse.response.docs);
    } 
    catch (parseError) {
      console.error("Error parsing shell script output:", parseError);
      return res.status(500).json({ error: "500 - Failed to parse shell script output as JSON" });
    }
  });
});

/**
 * Route to get a specific number of monuments, mainly to display in the homepage
 * 'number' muste be an element present in the requ body, indicating how many monuments are to be sent. If not present, the request will be ignored
 * 
 * Returns only the name and image URL for every monument 
 */
app.post("/monuments", (req: any, res: any) => {
  if (!req.body) {
    return res.status(400).send("400 - No body found in the request");
  } 

  const { number } = req.body;

  if (!number) {
    return res.status(400).json({ error: "400 - No number was provided in the body request" });
  }

  const queryJson = JSON.stringify({
    "query": "*:*",
    "params": {
      "fl": "id, Nome, Localizacao",
      "rows": 20
    }
  });

  execFile(scriptPath, [solrUrl, queryJson], (error, stdout, stderr) => {
    if (error) {
      console.error("Error executing shell script:", error);
      return res.status(500).json({ error: "500 - Internal Server Error executing shell script" });
    }

    if (stderr) {
      console.error("Shell script error:", stderr);
      return res.status(500).json({ error: "500 - Internal Server Error in the shell script: " + error});
    }

    try {
      const jsonResponse = JSON.parse(stdout);

      console.log(jsonResponse.response.docs);

      return res.status(200).json(jsonResponse.response.docs);
    } 
    catch (parseError) {
      console.error("Error parsing shell script output:", parseError);
      return res.status(500).json({ error: "500 - Failed to parse shell script output as JSON" });
    }
  });
});

/**
 * Route to get a specific monument data, to display in an individual page
 * 'id' must be present in the req body. If not present, the request will be ignored
 * 
 * Retuns all the fields stored for each monument
 */
app.post("/monument", (req: any, res: any) => {
  if (!req.body){
    return res.status(400).send("400 - No body found in the request");
  }

  const { id } = req.body;

  if (!id) {
    return res.status(400).json({error: "400 - No id was provided in the body request"});
  }

  const queryJson = JSON.stringify({
    "query": "id:" + id.toString()
  });

  execFile(scriptPath, [solrUrl, queryJson], (error, stdout, stderr) => {
    if (error) {
      console.error("Error executing shell script:", error);
      return res.status(500).json({ error: "500 - Internal Server Error executing shell script" });
    }

    if (stderr) {
      console.error("Shell script error:", stderr);
      return res.status(500).json({ error: "500 - Internal Server Error in the shell script: " + error});
    }

    try {
      const jsonResponse = JSON.parse(stdout);

      console.log(jsonResponse.response.docs);

      return res.status(200).json(jsonResponse.response.docs);
    } 
    catch (parseError) {
      console.error("Error parsing shell script output:", parseError);
      return res.status(500).json({ error: "500 - Failed to parse shell script output as JSON" });
    }
  });
});

app.listen(port, () => {
  console.log(`[server]: Server is running at http://localhost:${port}`);
});