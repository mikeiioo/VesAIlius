import { useState } from "react";
import { FiSearch } from "react-icons/fi"; // Import search icon

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState("");
  const [isPressed, setIsPressed] = useState(false); // Track if Enter key is pressed

  const handleSearch = () => {
    if (query.trim() !== "") {
      onSearch(query); // Execute search if query is filled
      setIsPressed(true);
      setTimeout(() => setIsPressed(false), 200); // Reset button color after animation
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch(); // Search when Enter is pressed
    }
  };

  return (
    <div className="flex justify-center mt-6">
      {/* Search Bar Container */}
      <div className="flex items-center border border-gray-300 rounded-full shadow-md p-2 w-96">
        {/* Input Field */}
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyPress} // Detect Enter key press
          placeholder="Search datasets..."
          className="outline-none w-full px-3 text-gray-700 text-lg"
        />

        {/* Search Icon (Button) */}
        <button
          onClick={handleSearch}
          className={`p-3 text-white rounded-full transition-all flex items-center justify-center ${
            isPressed ? "bg-blue-700" : "bg-blue-500 hover:bg-blue-600"
          }`}
        >
          <FiSearch size={24} />
        </button>
      </div>
    </div>
  );
};

export default SearchBar;