import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';

import MonumentDetail from './MonumentDetail';

function Home() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredItems, setFilteredItems] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  // Mock data for demonstration
  const mockMonument = [
    {
      id: 1,
      Nome: "Castelo de Santa Maria da Feira",
      Descricao: "O Castelo da Feira, também referido como Castelo de Santa Maria da Feira e Castelo de Santa Maria...",
      Historia: "Embora a primitiva ocupação humana do seu sítio remonte à pré-história...",
      Tipo: "castelo património cultural",
      Estilo: "arquitetura românica",
      EstatutoPatrimonial: "Monumento Nacional",
      Localizacao: "Santa Maria da Feira, Travanca, Sanfins e Espargo, Portugal",
      Coordenadas: null,
      URLImagem: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Castelo_da_Feira.jpg/275px-Castelo_da_Feira.jpg"
    }
  ];

  const sendRequest = async () => {
    try {
      const response = await fetch('http://localhost:5001/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ number: 20 })
      });
      const data = await response.json();
      console.log('Response:', data);
    } catch (error) {
      console.error('Error sending request:', error);
    }
  };s

  const handleSearch = (e) => {
    e.preventDefault();
    setErrorMessage("");

    const filteredResults = mockMonument.filter((item) =>
      item.Nome.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (filteredResults.length > 0) {
      setFilteredItems(filteredResults);
    } else {
      setFilteredItems([]);
      setErrorMessage("No results found.");
    }
  };

  const navigate = useNavigate();

  return (
    <div className="App bg-gray-100 min-h-screen flex flex-col items-center justify-center">
      <header className="text-center">
        <form onSubmit={sendRequest} className="mt-8 flex items-center space-x-4">
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
