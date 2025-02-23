const DatasetDetails = ({ dataset }) => {
    if (!dataset) return <p>No dataset selected.</p>;
  
    return (
      <div className="p-4 border rounded">
        <h2 className="text-2xl font-bold">{dataset.title}</h2>
        <p>{dataset.summary}</p>
        <a href={dataset.url} target="_blank" rel="noopener noreferrer" className="text-blue-500">
          View Full Dataset
        </a>
      </div>
    );
  };
  
  export default DatasetDetails;  