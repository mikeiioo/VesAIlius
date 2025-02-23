import axios from 'axios';

const API_BASE_URL = "http://127.0.0.1:5000";

export const searchDatasets = async (query) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/search`, { params: { query } });
    return response.data;
  } catch (error) {
    console.error("Error fetching datasets:", error);
    return [];
  }
};