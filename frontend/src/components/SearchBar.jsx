import { useState } from "react";
import { FiSearch } from "react-icons/fi"; // Import search icon

const SearchBar = ({ onSearch }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    if (query.trim() !== "") {
      onSearch(query);  // Execute search if query is filled
      setIsExpanded(true); // Keep the search bar expanded
    } else {
      setIsExpanded(!isExpanded); // Toggle expansion only if empty
    }
  };

  return (
    <div className="flex justify-center mt-6">
      {/* Search Bar Container */}
      <div
        className={`flex items-center border border-gray-300 rounded-full shadow-md transition-all duration-300 ease-in-out ${
          isExpanded ? "w-72 p-2" : "w-12 p-2 justify-center"
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
          className="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-all flex items-center justify-center"
        >
          <FiSearch size={20} />
        </button>
      </div>
    </div>
  );
};

export default SearchBar;