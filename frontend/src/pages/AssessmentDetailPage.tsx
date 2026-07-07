import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { api } from "../services/api";
import type { Assessment } from "../types/assessment";

export default function AssessmentDetailPage() {
  const { vendorId } = useParams();
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!vendorId) {
      setError("No vendor ID was provided.");
      setLoading(false);
      return;
    }

    api
      .get<Assessment>(`/assessments/${vendorId}`)
      .then((response) => setAssessment(response.data))
      .catch(() => setError("Assessment not found."))
      .finally(() => setLoading(false));
  }, [vendorId]);

  if (loading) {
    return <p>Loading assessment details...</p>;
  }

  if (error || !assessment) {
    return (
      <section>
        <p>{error || "Assessment not found."}</p>
        <Link to="/">Return to dashboard</Link>
      </section>
    );
  }

  return (
    <section>
      <Link to="/">← Back to dashboard</Link>

      <h1>{assessment.vendor.vendor_name}</h1>
      <p>
        {assessment.vendor.industry} · {assessment.vendor.criticality} criticality
      </p>

      <div style={{ display: "flex", gap: "2rem", margin: "2rem 0" }}>
        <div>
          <strong>Risk score</strong>
          <p style={{ fontSize: "2rem", margin: "0.5rem 0" }}>
            {assessment.risk_score}
          </p>
        </div>

        <div>
          <strong>Risk tier</strong>
          <p style={{ fontSize: "2rem", margin: "0.5rem 0" }}>
            {assessment.risk_tier}
          </p>
        </div>

        <div>
          <strong>Assessment ID</strong>
          <p>{assessment.assessment_id}</p>
        </div>
      </div>

      <h2>Risk drivers</h2>
      <ul>
        {assessment.reasons.map((reason) => (
          <li key={reason}>{reason}</li>
        ))}
      </ul>

      <h2>Assessment metadata</h2>
      <p>
        <strong>Created:</strong>{" "}
        {new Date(assessment.created_at).toLocaleString()}
      </p>
      <p>
        <strong>Scoring version:</strong> {assessment.scoring_version}
      </p>

      <h2>Vendor profile</h2>
      <ul>
        <li>
          <strong>Data type:</strong> {assessment.vendor.data_type}
        </li>
        <li>
          <strong>Hosts PII:</strong>{" "}
          {assessment.vendor.hosts_pii ? "Yes" : "No"}
        </li>
        <li>
          <strong>SOC 2:</strong>{" "}
          {assessment.vendor.has_soc2 ? "Available" : "Not available"}
        </li>
        <li>
          <strong>ISO 27001:</strong>{" "}
          {assessment.vendor.has_iso27001 ? "Available" : "Not available"}
        </li>
        <li>
          <strong>MFA:</strong>{" "}
          {assessment.vendor.mfa_enabled ? "Enabled" : "Not enabled"}
        </li>
        <li>
          <strong>Encryption at rest:</strong>{" "}
          {assessment.vendor.encryption_at_rest ? "Enabled" : "Not enabled"}
        </li>
        <li>
          <strong>Incident response plan:</strong>{" "}
          {assessment.vendor.incident_response_plan
            ? "Available"
            : "Not available"}
        </li>
        <li>
          <strong>Subprocessors:</strong> {assessment.vendor.subprocessors_count}
        </li>
      </ul>
    </section>
  );
}