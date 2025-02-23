import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Papa from 'papaparse';

const DatasetPage = () => {
  const { datasetId } = useParams();
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [csvData, setCsvData] = useState(null);
  const [summary, setSummary] = useState('');
  const [selectedColumns, setSelectedColumns] = useState([]);
  const [columnOrder, setColumnOrder] = useState([]);

  useEffect(() => {
    const fetchDataset = async () => {
      try {

        // Fetch dataset details first to get the URL for the CSV data
        const datasetResponse = await axios.get(`http://127.0.0.1:5000/dataset/${datasetId}`);
        setDataset(datasetResponse.data);

        console.log("FETCHING MAIN DATA:", datasetId);
        // Fetch summary and CSV data concurrently
        const [summaryResponse, csvResponse] = await Promise.all([
          axios.get(`http://127.0.0.1:5000/summary/${datasetId}`),
          axios.get(`http://127.0.0.1:5000/fetch_csv`, {
            params: { url: datasetResponse.data.url },
            responseType: 'blob' // Ensure the response is treated as a blob
          })
        ]);

        console.log("SUMMARY RESPONSE:", summaryResponse.data);
        setSummary(summaryResponse.data.summary);

        console.log("FINISHED FETCHING CSV:");
        const csvText = await csvResponse.data.text();

        // Parse CSV data
        const parsedData = Papa.parse(csvText, { header: true });

        // Set CSV data
        setCsvData(parsedData.data);
        const columns = Object.keys(parsedData.data[0]);
        setSelectedColumns(columns); // Initialize selected columns with all columns
        setColumnOrder(columns); // Store the original column order
        console.log("SET CSV DATA");
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
      <p>{summary}</p>
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