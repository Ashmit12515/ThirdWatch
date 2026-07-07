import { useEffect, useState } from "react";
import { api } from "./services/api";

type Assessment = {
  assessment_id: string;
  risk_score: number;
  risk_tier: string;
  created_at: string;
  vendor: {
    vendor_name: string;
    industry: string;
  };
};

function App() {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<Assessment[]>("/assessments/")
      .then((response) => setAssessments(response.data))
      .catch((error) => console.error("Failed to fetch assessments:", error))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main style={{ maxWidth: "1100px", margin: "0 auto", padding: "2rem" }}>
      <h1>Vendor Risk Governance</h1>
      <p>Explainable vendor assessments with audit metadata.</p>

      {loading ? (
        <p>Loading assessments...</p>
      ) : assessments.length === 0 ? (
        <p>No assessments yet. Create one through Postman first.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th align="left">Vendor</th>
              <th align="left">Industry</th>
              <th align="left">Score</th>
              <th align="left">Tier</th>
              <th align="left">Assessment ID</th>
            </tr>
          </thead>
          <tbody>
            {assessments.map((assessment) => (
              <tr key={assessment.assessment_id}>
                <td>{assessment.vendor.vendor_name}</td>
                <td>{assessment.vendor.industry}</td>
                <td>{assessment.risk_score}</td>
                <td>{assessment.risk_tier}</td>
                <td>{assessment.assessment_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}

export default App;