import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function MonumentDetail() {
  const { id } = useParams(); // Extract ID from URL
  const navigate = useNavigate();

  const [monument, setMonument] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMonument = async () => {
      try {
        const response = await fetch('http://localhost:5001/monument', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id }),
        });

        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();
        const monumentData = data.response.docs[0]; // Assuming Solr always returns docs in an array

        if (monumentData) {
          setMonument({
            id: monumentData.id,
            Nome: monumentData.Nome,
            Localizacao: monumentData.Localizacao || "Location not available",
            URLImagem: monumentData.URL_Imagem || "https://via.placeholder.com/150",
            Descricao: monumentData.Descricao || "Description not available",
            Historia: monumentData.Historia || "History not available",
            Tipo: monumentData.Tipo || "Type not available",
            Estilo: monumentData.Estilo || "Style not available",
            EstatutoPatrimonial: monumentData.Estatuto_Patrimonial || "Status not available",
          });
        } else {
          setErrorMessage("Monument details not found.");
        }
      } catch (error) {
        console.error("Error fetching monument:", error);
        setErrorMessage("Failed to fetch monument details. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchMonument();
  }, [id]);

  if (loading) {
    return <p className="text-center mt-8">Loading...</p>;
  }

  if (errorMessage) {
    return <p className="text-center text-red-500 mt-8">{errorMessage}</p>;
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
        <p className="text-gray-600 mb-4"><strong>Localização: </strong>{monument.Localizacao}</p>
        <p className="mb-2"><strong>Descrição:</strong> {monument.Descricao}</p>
        <p className="mb-2"><strong>História:</strong> {monument.Historia}</p>
        <p className="mb-2"><strong>Tipo:</strong> {monument.Tipo}</p>
        <p className="mb-2"><strong>Estilo:</strong> {monument.Estilo}</p>
        <p className="mb-2"><strong>Estatuto Patrimonial:</strong> {monument.EstatutoPatrimonial}</p>
      </div>
    </div>
  );
}

export default MonumentDetail;
