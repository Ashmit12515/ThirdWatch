import { BrowserRouter, Link, Route, Routes } from "react-router-dom";

import DashboardPage from "./pages/DashboardPage";
import NewAssessmentPage from "./pages/NewAssessmentPage";

function App() {
  return (
    <BrowserRouter>
      <main style={{ maxWidth: "1100px", margin: "0 auto", padding: "2rem" }}>
        <nav style={{ display: "flex", gap: "1rem", marginBottom: "2rem" }}>
          <Link to="/">Dashboard</Link>
          <Link to="/assessments/new">New Assessment</Link>
        </nav>

        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/assessments/new" element={<NewAssessmentPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;