const DatasetList = ({ datasets }) => {
  return (
    <div className="p-4 bg-gray-900 text-white min-h-screen">
      {datasets.length === 0 ? <p>No results found.</p> : datasets.map((dataset) => (
        <div key={dataset.url} className="border border-gray-700 p-4 rounded mb-2 bg-gray-800">
          <h2 className="text-xl font-bold">{dataset.title}</h2>
          <p>{dataset.summary}</p>
          <a href={dataset.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
            View Dataset
          </a>
        </div>
      ))}
    </div>
  );
};

export default DatasetList;