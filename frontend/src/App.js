import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import DatasetPage from "./pages/DatasetPage";

const App = () => {
  return (
    <Router>
      <div className="max-w-3xl mx-auto p-4">
        <h1 className="text-3xl font-bold text-center mb-4">Vesalius Dataset Search</h1>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dataset/:datasetId" element={<DatasetPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;