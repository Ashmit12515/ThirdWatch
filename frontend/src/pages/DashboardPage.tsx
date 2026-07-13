import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../services/api";
import type { Assessment } from "../types/assessment";

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

  const summary = useMemo(() => {
    return {
      total: assessments.length,
      tier1: assessments.filter(
        (assessment) => assessment.risk_tier === "Tier 1",
      ).length,
      tier2: assessments.filter(
        (assessment) => assessment.risk_tier === "Tier 2",
      ).length,
      tier3: assessments.filter(
        (assessment) => assessment.risk_tier === "Tier 3",
      ).length,
    };
  }, [assessments]);

  return (
    <section>
      <div className="page-header dashboard-header">
        <div>
          <h1>Vendor Risk Governance</h1>
          <p>Explainable vendor assessments with audit metadata.</p>
        </div>

        <Link className="primary-link" to="/assessments/new">
          New assessment
        </Link>
      </div>

      <div className="summary-grid">
        <article className="summary-card">
          <span>Total assessments</span>
          <strong>{summary.total}</strong>
        </article>

        <article className="summary-card tier-1-card">
          <span>Tier 1 risk</span>
          <strong>{summary.tier1}</strong>
        </article>

        <article className="summary-card tier-2-card">
          <span>Tier 2 risk</span>
          <strong>{summary.tier2}</strong>
        </article>

        <article className="summary-card tier-3-card">
          <span>Tier 3 risk</span>
          <strong>{summary.tier3}</strong>
        </article>
      </div>

      {loading ? (
        <p>Loading assessments...</p>
      ) : assessments.length === 0 ? (
        <div className="empty-state">
          <h2>No assessments yet</h2>

          <p>
            Create your first vendor assessment to populate the dashboard.
          </p>

          <Link className="primary-link" to="/assessments/new">
            Create assessment
          </Link>
        </div>
      ) : (
        <div className="table-card">
          <table>
            <thead>
              <tr>
                <th>Vendor</th>
                <th>Vendor ID</th>
                <th>Industry</th>
                <th>Score</th>
                <th>Tier</th>
                <th>Assessment ID</th>
              </tr>
            </thead>

            <tbody>
              {assessments.map((assessment) => (
                <tr key={assessment.assessment_id}>
                  <td>
                    <Link
                      to={`/assessments/${assessment.vendor.vendor_id}`}
                    >
                      {assessment.vendor.vendor_name}
                    </Link>
                  </td>

                  <td>
                    <code>{assessment.vendor.vendor_id}</code>
                  </td>

                  <td>{assessment.vendor.industry}</td>

                  <td>{assessment.risk_score}</td>

                  <td>
                    <span
                      className={`tier-badge ${assessment.risk_tier
                        .toLowerCase()
                        .replace(" ", "-")}`}
                    >
                      {assessment.risk_tier}
                    </span>
                  </td>

                  <td>{assessment.assessment_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}