import React, { useState } from 'react';
import SearchBar from "../components/SearchBar";
import { useNavigate } from "react-router-dom";
import { searchDatasets } from "../api";

const HomePage = () => {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(false); // Track loading state
  const [searched, setSearched] = useState(false); // Track if search was performed
  const navigate = useNavigate();

  const handleSearch = async (query) => {
    setLoading(true);
    setSearched(true); // Mark that a search has been performed
    console.log("SEARCHING FOR:", query);
    const results = await searchDatasets(query);
    console.log("RESULTS", results);
    setDatasets(results);
    setLoading(false);
  };

  const handleDatasetClick = (dataset) => {
    console.log("CLICKED ON DATASET:", dataset);
    navigate(`/dataset/${dataset.id}`);
    setSearched(false); // Mark that user has left page
  };

  return (
    <div className="p-8 text-center">
      <h1 className="text-4xl font-bold mb-4">Welcome to VesAIlius</h1>
      <p className="text-gray-600 mb-6">Search and explore AI-powered CDC datasets.</p>
      <SearchBar onSearch={handleSearch} />

      {/* Show loading indicator while fetching results */}
      {loading && (
        <div className="flex justify-center mt-6">
          <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500"></div>
        </div>
      )}

      {/* Show Featured Datasets ONLY when datasets exist */}
      {datasets.length > 0 && !loading && (
        <div className="mt-6">
          <h2 className="text-2xl font-bold">Featured Datasets</h2>
          <div className="grid grid-cols-1 gap-4 mt-4">
            {datasets.map((dataset) => (
              <div
                key={dataset.id}
                onClick={() => handleDatasetClick(dataset)}
                className="border p-4 rounded cursor-pointer hover:bg-gray-100"
              >
                <h3 className="text-xl font-semibold">{dataset.title}</h3>
                <p>{dataset.summary}</p>
              </div>
            ))}
          </div> 
        </div>
      )}

      {/* Show No Results Message if No Datasets Found and a Search was Performed */}
      {!loading && searched && datasets.length === 0 && (
        <div className="mt-6 flex flex-col items-center">
          <p className="text-xl text-gray-500">🚫 No results found. Try a different search.</p>
        </div>
      )}
    </div>
  );
};

export default HomePage;