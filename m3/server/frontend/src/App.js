import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    console.log('Search Term:', searchTerm);
  };

  return (
    <div className="App bg-gray-100 min-h-screen flex flex-col items-center justify-center">
      <header className="text-center">
        <img src={logo} className="App-logo mx-auto" alt="logo" />
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
        <p className="mt-4 text-gray-600">
          Edit <code className="bg-gray-200 p-1 rounded">src/App.js</code> and save to reload.
        </p>
        <a
          className="text-blue-500 underline mt-2 inline-block"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
