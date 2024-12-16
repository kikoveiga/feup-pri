import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';

import MonumentDetail from './MonumentDetail';

function Home() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredItems, setFilteredItems] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  const sendRequest = async () => {
    if (!searchTerm.trim()) {
      setErrorMessage("Search term cannot be empty.");
      return;
    }
    try {
      const response = await fetch('http://localhost:5001/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchTerm, number: 20 }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status} - ${response.statusText}`);
      }
  
      const data = await response.json();
      console.log('Response:', data);
  
      // Map Solr data to the frontend's expected format
      const mappedItems = data.response.docs.map((doc) => ({
        id: doc.id,
        Nome: doc.Nome,
        Historia: doc.Historia,
        Localizacao: doc.Localizacao || "Location not available", // Handle missing values
        URLImagem: doc.URL_Imagem || "https://via.placeholder.com/150", // Handle the space in the key
      }));
      
      setFilteredItems(mappedItems);
    } catch (error) {
      console.error('Error in sendRequest:', error);
      setErrorMessage('Failed to fetch data. Please try again.');
    }
  };
  
  

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page reload
    setErrorMessage(""); // Clear any existing errors
    sendRequest(); // Call the async request
  };
  

  const navigate = useNavigate();

  return (
    <div className="App bg-gray-100 min-h-screen flex flex-col items-center justify-center">
      <header className="text-center">
        <form onSubmit={handleSubmit} className="mt-8 flex items-center space-x-4">
          <input
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-64 p-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition duration-300">
            Search
          </button>
        </form>
      </header>

      {errorMessage && <p className="text-red-500 mt-4">{errorMessage}</p>}

      <div className="mt-8 w-full max-w-xl">
        <ul className="bg-white shadow rounded-lg p-4">
          {filteredItems.length > 0 ? (
            filteredItems.map((item) => (
              <li
                key={item.id}
                className="py-4 border-b last:border-b-0 flex items-center space-x-4 cursor-pointer hover:bg-gray-100"
                onClick={() => navigate(`/monument/${item.id}`, { state: item })}
              >
                <img
                  src={item.URLImagem}
                  alt={item.Nome}
                  className="w-24 h-24 object-cover rounded-lg shadow-md"
                />
                <div>
                  <h3 className="font-bold text-lg">{item.Nome}</h3>
                  <p className="text-sm text-gray-600">{item.Localizacao}</p>
                </div>
              </li>
            ))
          ) : (
            <p className="text-gray-500 text-center">No results found.</p>
          )}
        </ul>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/monument/:id" element={<MonumentDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
