import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import DatasetPage from "./pages/DatasetPage";
import { Link } from "react-router-dom";

const App = () => {
  return (
    <Router>
      <div className="max-w-3xl mx-auto p-4">
        {/* Make the h1 a link to the homepage */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dataset/:datasetId" element={<DatasetPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;