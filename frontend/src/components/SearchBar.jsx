import { useState } from "react";
import { FiSearch } from "react-icons/fi"; // Import search icon

const SearchBar = ({ onSearch }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    if (isExpanded && query.trim() !== "") {
      onSearch(query); // Execute search only if expanded & query is not empty
    }
    setIsExpanded(!isExpanded); // Toggle expansion
  };

  return (
    <div className="flex items-center justify-center mt-4">
      {/* Search Bar Container */}
      <div
        className={`flex items-center border border-gray-300 rounded-full shadow-md transition-all duration-300 ease-in-out ${
          isExpanded ? "w-72 p-2" : "w-12 p-2"
        }`}
      >
        {/* Input Field */}
        {isExpanded && (
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search datasets..."
            className="outline-none w-full px-3 text-gray-700"
          />
        )}

        {/* Search Icon (Button) */}
        <button
          onClick={handleSearch}
          className="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-all"
        >
          <FiSearch size={20} />
        </button>
      </div>
    </div>
  );
};

export default SearchBar;