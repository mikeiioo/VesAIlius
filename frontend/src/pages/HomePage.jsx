import SearchBar from "../components/SearchBar";

const HomePage = ({ onSearch }) => {
  return (
    <div className="p-8 text-center">
      <h1 className="text-4xl font-bold mb-4">Welcome to VesAIlius</h1>
      <p className="text-gray-600 mb-6">Search and explore AI-powered CDC datasets.</p>
      <SearchBar onSearch={onSearch} />
    </div>
  );
};

export default HomePage;