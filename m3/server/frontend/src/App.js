import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';

import MonumentDetail from './MonumentDetail';

function Home() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredItems, setFilteredItems] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [number, setNumber] = useState(20); // Number of results to show

  const sendRequest = async () => {
    if (!searchTerm.trim()) {
      setErrorMessage("Search term cannot be empty.");
      return;
    }
    try {
      const response = await fetch('http://localhost:5001/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchTerm, number }),
      });

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();

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

  const handleNumberChange = () => {
    const newNumber = prompt("Enter the number of monuments to display:", number);
    if (newNumber && !isNaN(newNumber)) {
      setNumber(parseInt(newNumber, 10));
    }
  };

  const navigate = useNavigate();

  return (
    <div className="App bg-gray-100 min-h-screen flex flex-col items-center justify-center">
    <header className="text-center w-full max-w-3xl">
      <form onSubmit={handleSubmit} className="mt-8 flex flex-col items-center space-y-4">
        <input
          type="text"
          placeholder="Search for monuments..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full p-3 text-lg rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
        <div className="flex space-x-4">
          <button type="submit" className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition duration-300">
            Search
          </button>
          <button
            type="button"
            onClick={handleNumberChange}
            className="bg-gray-500 text-white px-6 py-2 rounded-md hover:bg-gray-600 transition duration-300"
          >
            Results: {number}
          </button>
        </div>
      </form>
    </header>
  
    {errorMessage && <p className="text-red-500 mt-4">{errorMessage}</p>}
  
    <div className="mt-8 w-full max-w-5xl grid grid-cols-2 gap-6">
      {filteredItems.length > 0 ? (
        filteredItems.map((item) => (
          <div
            key={item.id}
            className="bg-white shadow rounded-lg p-4 flex flex-col items-center cursor-pointer hover:bg-gray-100"
            onClick={() => navigate(`/monument/${item.id}`, { state: item })}
          >
            <img
              src={item.URLImagem}
              alt={item.Nome}
              className="w-32 h-32 object-cover rounded-lg shadow-md mb-4"
            />
            <div className="text-center">
              <h3 className="font-bold text-lg">{item.Nome}</h3>
              <p className="text-sm text-gray-600">{item.Localizacao}</p>
            </div>
          </div>
        ))
      ) : (
        <p className="text-gray-500 text-center col-span-2">No results found.</p>
      )}
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
