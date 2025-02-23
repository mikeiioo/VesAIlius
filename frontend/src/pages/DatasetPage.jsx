import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const DatasetPage = () => {
  const { datasetId } = useParams();
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDataset = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/dataset/${datasetId}`);
        setDataset(response.data);
      } catch (error) {
        console.error("Error fetching dataset:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDataset();
  }, [datasetId]);

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
    </div>
  );
};

export default DatasetPage;