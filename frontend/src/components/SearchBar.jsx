import { useState } from "react";

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  return (
    <div className="p-4 flex flex-col items-center">
      {/* Search Input Field */}
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for datasets..."
        className="p-3 border rounded w-full md:w-3/4 text-lg"
      />
      
      {/* Search Button */}
      <button
        onClick={() => onSearch(query)}
        className="mt-3 p-2 bg-blue-600 text-white rounded-lg shadow-md w-full md:w-3/4 hover:bg-blue-700 transition"
      >
        Search
      </button>
    </div>
  );
};

export default SearchBar;