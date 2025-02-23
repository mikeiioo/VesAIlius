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
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="p-8 text-center">
        <h1 className="text-4xl font-bold mb-4">Welcome to Vesalius</h1>
        <p className="text-gray-400 mb-6">AI-powered exploration of CDC datasets.</p>

        <SearchBar onSearch={handleSearch} />

        {/* What is Vesalius? Section - Disappears After Search */}
        {!searched && (
          <div className="bg-gray-800 shadow-md rounded-full p-6 max-w-2xl mx-auto mt-6">
            <h2 className="text-2xl font-bold text-gray-200">What is Vesalius?</h2>
            <p className="text-gray-400 mt-2">
              Vesalius is an AI-driven tool that helps users discover, summarize, and explore CDC datasets with ease. 
              Utilizing advanced search and ranking algorithms, it allows seamless interaction with large-scale public health data.
            </p>
          </div>
        )}

        {/* Show loading indicator while fetching results */}
        {loading && (
          <div className="flex justify-center mt-6">
            <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500"></div>
          </div>
        )}

        {/* Show Featured Datasets ONLY when datasets exist */}
        {datasets.length > 0 && !loading && (
          <div className="mt-6">
            <h2 className="text-2xl font-medium text-gray-100">Relevant Datasets</h2>
            <div className="grid grid-cols-1 gap-4 mt-4">
              {datasets.map((dataset, index) => (
                <div
                  key={dataset.id}
                  onClick={() => handleDatasetClick(dataset)}
                  className="border border-gray-700 p-4 rounded cursor-pointer bg-gray-800 hover:bg-gray-700 relative pl-10 pr-10" // Added padding-left
                >
                  <span className="absolute top-2 left-2 text-blue-400 text-lg font-bold opacity-50">
                    {index + 1}
                  </span>
                  <h3 className="text-xl font-semibold text-gray-300">{dataset.title}</h3>
                  <p className="text-gray-400">{dataset.summary}</p>
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
    </div>
  );
};

export default HomePage;