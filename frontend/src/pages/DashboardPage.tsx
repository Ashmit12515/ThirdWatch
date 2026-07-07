import { useEffect, useState } from "react";
import { api } from "../services/api";
import type { Assessment } from "../types/assessment";
import { Link } from "react-router-dom";
export default function DashboardPage() {
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
    <section>
      <h1>Vendor Risk Governance</h1>
      <p>Explainable vendor assessments with audit metadata.</p>

      {loading ? (
        <p>Loading assessments...</p>
      ) : assessments.length === 0 ? (
        <p>No assessments yet. Create your first assessment.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Vendor</th>
              <th>Industry</th>
              <th>Score</th>
              <th>Tier</th>
              <th>Assessment ID</th>
            </tr>
          </thead>
          <tbody>
            {assessments.map((assessment) => (
              <tr key={assessment.assessment_id}>
                <td><Link to={`/assessments/${assessment.vendor.vendor_id}`}>
                {assessment.vendor.vendor_name}
                </Link>
                </td>
                <td>{assessment.vendor.industry}</td>
                <td>{assessment.risk_score}</td>
                <td>{assessment.risk_tier}</td>
                <td>{assessment.assessment_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}