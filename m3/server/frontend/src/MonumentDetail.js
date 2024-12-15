import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function MonumentDetail() {
  const location = useLocation();
  const navigate = useNavigate();

  // Access monument data passed via "state"
  const monument = location.state;

  if (!monument) {
    return <p className="text-center text-red-500 mt-8">Monument details not available.</p>;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-8">
      <button
        onClick={() => navigate(-1)}
        className="mb-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition duration-300"
      >
        Back
      </button>
      <div className="bg-white shadow-lg rounded-lg p-6 max-w-4xl w-full">
        <img
          src={monument.URLImagem}
          alt={monument.Nome}
          className="w-full h-64 object-cover rounded-md mb-4"
        />
        <h1 className="text-2xl font-bold mb-2">{monument.Nome}</h1>
        <p className="text-gray-600 mb-4">{monument.Localizacao}</p>
        <p className="mb-2"><strong>Description:</strong> {monument.Descricao}</p>
        <p className="mb-2"><strong>History:</strong> {monument.Historia}</p>
        <p className="mb-2"><strong>Type:</strong> {monument.Tipo}</p>
        <p className="mb-2"><strong>Style:</strong> {monument.Estilo}</p>
        <p><strong>Status:</strong> {monument.EstatutoPatrimonial}</p>
      </div>
    </div>
  );
}

export default MonumentDetail;
