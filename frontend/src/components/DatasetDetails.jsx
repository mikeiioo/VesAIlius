import { useEffect, useState } from "react";
import axios from "axios";

const DatasetDetails = ({ match }) => {
    const [dataset, setDataset] = useState(null);
    const datasetId = match.params.id; // Assuming the dataset ID is passed as a URL parameter

    useEffect(() => {
        const fetchDataset = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/dataset/${datasetId}`);
                setDataset(response.data);
            } catch (error) {
                console.error("Error fetching dataset details:", error);
            }
        };

        fetchDataset();
    }, [datasetId]);

    if (!dataset) return <p>Loading dataset details...</p>;

    return (
        <div className="p-4">
            <h2 className="text-2xl font-bold">{dataset.title}</h2>
            <p>{dataset.summary}</p>
            <a href={dataset.url} target="_blank" rel="noopener noreferrer" className="text-blue-500">
                View Full Dataset
            </a>
            {/* Additional dataset content can be displayed here */}
        </div>
    );
};

export default DatasetDetails;