const DatasetList = ({ datasets }) => {
  return (
    <div className="p-4">
      {datasets.length === 0 ? <p>No results found.</p> : datasets.map((dataset) => (
        <div key={dataset.url} className="border p-4 rounded mb-2">
          <h2 className="text-xl font-bold">{dataset.title}</h2>
          <p>{dataset.summary}</p>
          <a href={dataset.url} target="_blank" rel="noopener noreferrer" className="text-blue-500">
            View Dataset
          </a>
        </div>
      ))}
    </div>
  );
};

export default DatasetList;