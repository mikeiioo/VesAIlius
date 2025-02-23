import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import DatasetDetails from "../components/DatasetDetails";

const DatasetPage = () => {
  const { datasetId } = useParams();
  const [dataset, setDataset] = useState(null);

  useEffect(() => {
    const fetchDataset = async () => {
      const response = await fetch(`http://127.0.0.1:5000/dataset/${datasetId}`);
      const data = await response.json();
      setDataset(data);
    };

    fetchDataset();
  }, [datasetId]);

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold">Dataset Details</h2>
      <DatasetDetails dataset={dataset} />
    </div>
  );
};

export default DatasetPage;