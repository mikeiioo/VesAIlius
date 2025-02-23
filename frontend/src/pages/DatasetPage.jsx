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
  const [columnsToExclude, setColumnsToExclude] = useState('');

  const title = datasetId.replaceAll('_', ' ').replaceAll(".csv", "");
  console.log(title)

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
        console.log("CSV", csvText)

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

  const handleDownloadFirst100 = async () => {
    if (!dataset?.file_name) {
      console.error("No file name found for dataset.");
      return;
    }
  
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/download_first_hundred`,
        {
          params: { file_name: dataset.file_name },
          responseType: 'blob'
        }
      );
  
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `first_100_${dataset.file_name}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Error downloading first 100 rows:", error);
    }
  };

  const handleDownloadFiltered = async () => {
    if (!dataset?.file_name) {
      console.error("No file name found for dataset.");
      return;
    }
  
    try {
      // Convert input to properly formatted comma-separated string
      const excludedColumns = columnsToExclude
        .split(',')
        .map(col => col.trim())
        .filter(col => col)
        .join(','); // Add this line to convert array back to string
  
      const response = await axios.get(
        `http://127.0.0.1:5000/download_all_exclude_columns`,
        {
          params: { 
            file_name: dataset.file_name,
            exclude_columns: excludedColumns // Use the joined string here
          },
          responseType: 'blob'
        }
      );
  
      // Add error handling for empty response
      if (!response.data) {
        throw new Error('Empty response from server');
      }
  
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `filtered_${dataset.file_name}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Error downloading filtered dataset:", error);
      // Add user feedback
      alert(`Download failed: ${error.message}`);
    }
  };

  if (loading) {
    return (
      <div className="p-8 bg-gray-900 min-h-screen flex flex-col items-center justify-center">
        <h2 className="text-2xl font-bold text-center">{title}</h2>
        <div className="flex justify-center mt-6">
          <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500"></div>
        </div>
      </div>
    )
  }

  if (!dataset) {
    return <p className="text-center text-gray-500">No dataset found.</p>;
  }

  return (
    <div className="p-8 bg-gray-900 min-h-screen">
      <h2 className="text-2xl font-bold text-center mb-4">{dataset.title}</h2>
      <p className="text-center text-gray-400 mb-6">{summary}</p>
      {/* Buttons for downloading dataset */}
      <div className="mt-4 flex flex-col items-center gap-4">
  {/* First row of buttons */}
  <div className="flex gap-4">
    <button
      onClick={handleDownloadFirst100}
      className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-all"
    >
      Download First 100 Rows
    </button>

    <a
      href={dataset.url}
      target="_blank"
      rel="noopener noreferrer"
      className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-all"
    >
      Download Entire Dataset
    </a>

    <button
      onClick={handleDownloadFiltered}
      className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-all"
    >
      Download Filtered Dataset
    </button>
  </div>

  {/* Column exclusion input */}
  <div className="w-full max-w-xl">
    <input
      type="text"
      placeholder="Columns to exclude (comma-separated, e.g., 'age,city,phone_number')"
      className="w-full px-4 py-2 rounded-lg border border-gray-600 bg-gray-800 text-white placeholder-gray-400"
      value={columnsToExclude}
      onChange={(e) => setColumnsToExclude(e.target.value)}
    />
    <p className="text-gray-400 text-sm mt-1 ml-1">
      Enter column names to exclude from the filtered download
    </p>
  </div>
</div>
      {csvData && (
        <>
          <div className="flex flex-wrap justify-center gap-2 mt-4">
            {columnOrder.map((key) => (
              <button
                key={key}
                onClick={() => toggleColumn(key)}
                className={`px-4 py-2 m-1 border rounded transition-colors duration-200 ${selectedColumns.includes(key) ? 'bg-blue-600 text-white border-blue-700 hover:bg-blue-500' : 'bg-gray-800 text-gray-300 border-gray-600 hover:bg-gray-700'}`}
              >
                {key}
              </button>
            ))}
          </div>
          <div className="overflow-x-auto mt-4">
            <table className="table-auto mx-auto bg-gray-800 text-gray-300">
              <thead>
                <tr>
                  {columnOrder.filter((key) => selectedColumns.includes(key)).map((key) => (
                    <th key={key} className="px-4 py-2 border border-gray-600">{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {csvData.slice(0, 100).map((row, index) => (
                  <tr key={index} className="hover:bg-gray-700">
                    {columnOrder.filter((key) => selectedColumns.includes(key)).map((key) => (
                      <td key={key} className="border border-gray-600 px-4 py-2">{row[key]}</td>
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