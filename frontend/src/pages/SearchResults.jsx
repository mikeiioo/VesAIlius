import DatasetList from "../components/DatasetList";

const SearchResults = ({ datasets }) => {
  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold">Search Results</h2>
      <DatasetList datasets={datasets} />
    </div>
  );
};

export default SearchResults;