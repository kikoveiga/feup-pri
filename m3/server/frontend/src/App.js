import React, { useState } from 'react';


function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredItems, setFilteredItems] = useState([]);

  const handleSearch = (e) => {
    e.preventDefault();

  };

  return (
    <div className="App bg-gray-100 min-h-screen flex flex-col items-center justify-center">
      <header className="text-center">
        <form
          onSubmit={handleSearch}
          className="mt-8 flex items-center space-x-4"
        >
          <input
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-64 p-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition duration-300"
          >
            Search
          </button>
        </form>
      </header>
    </div>
  );
}

export default App;
