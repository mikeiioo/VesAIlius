import { useState } from "react";
import { searchDatasets } from "./api";
import SearchBar from "./components/SearchBar";
import DatasetList from "./components/DatasetList";

const App = () => {
  const [datasets, setDatasets] = useState([]);

  const handleSearch = async (query) => {
    const results = await searchDatasets(query);
    setDatasets(results);
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-4">VesAIlius Dataset Search</h1>
      <SearchBar onSearch={handleSearch} />
      <DatasetList datasets={datasets} />
    </div>
  );
};

export default App;