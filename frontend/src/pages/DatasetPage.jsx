import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Papa from 'papaparse';

const DatasetPage = () => {
  const { datasetId } = useParams();
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [csvData, setCsvData] = useState(null);
  const [selectedColumns, setSelectedColumns] = useState([]);
  const [columnOrder, setColumnOrder] = useState([]);

  useEffect(() => {
    const fetchDataset = async () => {
      try {
        console.log("FETCHING DATASET:", datasetId);
        const response = await axios.get(`http://127.0.0.1:5000/dataset/${datasetId}`);
        console.log("DATASET RESPONSE:", response.data);
        setDataset(response.data);

        // Fetch the CSV data from the backend
        console.log("FETCHING CSV:", response.data.url);
        const csvResponse = await axios.get(`http://127.0.0.1:5000/fetch_csv`, {
          params: { url: response.data.url },
          responseType: 'blob' // Ensure the response is treated as a blob
        });
        console.log("FINISHED FETCHING CSV:");
        
        // Convert blob to text
        const csvText = await csvResponse.data.text();
        console.log("CSV TEXT:", csvText);

        // Parse CSV data
        const parsedData = Papa.parse(csvText, { header: true });
        console.log("PARSED CSV DATA:", parsedData.data);

        // Set CSV data
        setCsvData(parsedData.data);
        const columns = Object.keys(parsedData.data[0]);
        setSelectedColumns(columns); // Initialize selected columns with all columns
        setColumnOrder(columns); // Store the original column order
        console.log("SET CSV DATA:", parsedData.data);
      } catch (error) {
        console.error(`Error fetching dataset ${datasetId}:`, error);
      } finally {
        console.log("LOADING SET TO FALSE:", datasetId);
        setLoading(false);
      }
    };

    fetchDataset();
  }, [datasetId]);

  const toggleColumn = (column) => {
    setSelectedColumns((prevSelectedColumns) =>
      prevSelectedColumns.includes(column)
        ? prevSelectedColumns.filter((col) => col !== column)
        : [...prevSelectedColumns, column]
    );
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (!dataset) {
    return <p>No dataset found.</p>;
  }

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold">{dataset.title}</h2>
      <p>{dataset.summary}</p>
      <a href={dataset.url} target="_blank" rel="noopener noreferrer" className="text-blue-500">
        View Full Dataset
      </a>
      {csvData && (
        <>
          <div className="mt-4">
            {columnOrder.map((key) => (
              <button
                key={key}
                onClick={() => toggleColumn(key)}
                className={`px-4 py-2 m-1 border ${selectedColumns.includes(key) ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
              >
                {key}
              </button>
            ))}
          </div>
          <div className="overflow-x-auto mt-4">
            <table className="table-auto mx-auto">
              <thead>
                <tr>
                  {columnOrder.filter((key) => selectedColumns.includes(key)).map((key) => (
                    <th key={key} className="px-4 py-2 border">{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {csvData.slice(0, 100).map((row, index) => (
                  <tr key={index}>
                    {columnOrder.filter((key) => selectedColumns.includes(key)).map((key) => (
                      <td key={key} className="border px-4 py-2">{row[key]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
};

export default DatasetPage;