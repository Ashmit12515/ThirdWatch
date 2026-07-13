import { useEffect, useState } from "react";
import type { ChangeEvent } from "react";
import { Link, useParams } from "react-router-dom";

import { api } from "../services/api";
import type { Assessment } from "../types/assessment";

type EvidenceFile = {
  evidence_id: string;
  vendor_id: string;
  file_name: string;
  content_type: string | null;
  file_path: string;
  uploaded_at: string;
};

type ControlFinding = {
  control: string;
  status: string;
  evidence_text: string;
};

type EvidenceExtraction = {
  evidence_id: string;
  vendor_id: string;
  findings: ControlFinding[];
  extraction_method?: string;
  extracted_at?: string;
};

export default function AssessmentDetailPage() {
  const { vendorId } = useParams<{ vendorId: string }>();

  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [evidenceFiles, setEvidenceFiles] = useState<EvidenceFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [extractions, setExtractions] = useState<
    Record<string, EvidenceExtraction>
  >({});
  const [extractingEvidenceId, setExtractingEvidenceId] = useState<
    string | null
  >(null);

  const [recalculating, setRecalculating] = useState(false);
  const [recalculateMessage, setRecalculateMessage] = useState("");

  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");

  const loadPageData = async () => {
    if (!vendorId) return;

    try {
      setLoading(true);
      setError("");

      const [assessmentResponse, evidenceResponse] = await Promise.all([
        api.get<Assessment>(`/assessments/${vendorId}`),
        api.get<EvidenceFile[]>(`/evidence/${vendorId}`),
      ]);

      setAssessment(assessmentResponse.data);
      setEvidenceFiles(evidenceResponse.data);
    } catch (requestError) {
      console.error("Failed to load assessment details:", requestError);
      setError("Could not load the assessment details.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPageData();
  }, [vendorId]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;

    setSelectedFile(file);
    setUploadMessage("");
    setError("");
  };

  const handleUpload = async () => {
    if (!vendorId || !selectedFile) {
      setError("Choose a .txt or .pdf evidence file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setUploading(true);
      setError("");
      setUploadMessage("");

      const response = await api.post<EvidenceFile>(
        `/evidence/${vendorId}`,
        formData,
      );

      setEvidenceFiles((currentFiles) => [response.data, ...currentFiles]);
      setSelectedFile(null);
      setUploadMessage(`Uploaded ${response.data.file_name}.`);

      const fileInput = document.getElementById(
        "evidence-file",
      ) as HTMLInputElement | null;

      if (fileInput) {
        fileInput.value = "";
      }
    } catch (uploadError) {
      console.error("Evidence upload failed:", uploadError);
      setError("Upload failed. Only non-empty .txt and .pdf files are allowed.");
    } finally {
      setUploading(false);
    }
  };

  const handleExtractControls = async (evidenceId: string) => {
    try {
      setExtractingEvidenceId(evidenceId);
      setError("");

      const response = await api.get<EvidenceExtraction>(
        `/extractions/${evidenceId}`,
      );

      setExtractions((current) => ({
        ...current,
        [evidenceId]: response.data,
      }));
    } catch (extractionError) {
      console.error("Evidence extraction failed:", extractionError);
      setError("Could not extract controls from this evidence file.");
    } finally {
      setExtractingEvidenceId(null);
    }
  };

  const handleRecalculate = async () => {
    if (!vendorId) return;

    try {
      setRecalculating(true);
      setError("");
      setRecalculateMessage("");

      const response = await api.post<Assessment>(
        `/assessments/${vendorId}/recalculate`,
      );

      setAssessment(response.data);
      setRecalculateMessage(
        "Risk score recalculated using verified evidence controls.",
      );
    } catch (recalculateError) {
      console.error("Risk recalculation failed:", recalculateError);
      setError("Could not recalculate the risk score.");
    } finally {
      setRecalculating(false);
    }
  };

  if (loading) {
    return <p>Loading assessment details...</p>;
  }

  if (error && !assessment) {
    return (
      <section>
        <p className="error-message">{error}</p>
        <Link to="/">Return to dashboard</Link>
      </section>
    );
  }

  if (!assessment) {
    return null;
  }

  return (
    <section>
      <div className="page-header">
        <Link to="/">← Back to dashboard</Link>
        <h1>{assessment.vendor.vendor_name}</h1>
        <p>
          {assessment.vendor.industry} · {assessment.vendor.criticality}{" "}
          criticality
        </p>
      </div>

      <div className="detail-grid">
        <article className="detail-card">
          <span>Risk score</span>
          <strong>{assessment.risk_score}</strong>
        </article>

        <article className="detail-card">
          <span>Risk tier</span>
          <strong
            className={`tier-badge ${assessment.risk_tier
              .toLowerCase()
              .replace(" ", "-")}`}
          >
            {assessment.risk_tier}
          </strong>
        </article>

        <article className="detail-card">
          <span>Assessment ID</span>
          <strong>{assessment.assessment_id}</strong>
        </article>

        <article className="detail-card">
          <span>Scoring version</span>
          <strong>{assessment.scoring_version}</strong>
        </article>
      </div>

      <div className="detail-section">
        <h2>Risk rationale</h2>

        {assessment.reasons.length === 0 ? (
          <p className="muted-text">
            No active risk factors remain after evidence verification.
          </p>
        ) : (
          <ul className="reason-list">
            {assessment.reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        )}
      </div>

      <div className="detail-section evidence-section">
        <div>
          <h2>Evidence files</h2>
          <p>Upload SOC 2 reports, ISO certificates, or questionnaire notes.</p>
        </div>

        <div className="upload-row">
          <input
            id="evidence-file"
            type="file"
            accept=".txt,.pdf,text/plain,application/pdf"
            onChange={handleFileChange}
          />

          <button
            type="button"
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
          >
            {uploading ? "Uploading..." : "Upload evidence"}
          </button>
        </div>

        {uploadMessage && <p className="success-message">{uploadMessage}</p>}

        <div className="recalculate-row">
          <button
            type="button"
            onClick={handleRecalculate}
            disabled={recalculating || evidenceFiles.length === 0}
          >
            {recalculating
              ? "Recalculating..."
              : "Recalculate risk from evidence"}
          </button>

          {recalculateMessage && (
            <p className="success-message">{recalculateMessage}</p>
          )}
        </div>

        {error && <p className="error-message">{error}</p>}

        {evidenceFiles.length === 0 ? (
          <p className="muted-text">No evidence files uploaded yet.</p>
        ) : (
          <ul className="evidence-list">
            {evidenceFiles.map((file) => (
              <li key={file.evidence_id} className="evidence-item">
                <div className="evidence-file-info">
                  <strong>{file.file_name}</strong>
                  <span>
                    {file.content_type ?? "Unknown file type"} · Uploaded{" "}
                    {new Date(file.uploaded_at).toLocaleString()}
                  </span>
                </div>

                <div className="evidence-actions">
                  <span className="evidence-id">{file.evidence_id}</span>

                  <button
                    type="button"
                    className="secondary-button"
                    onClick={() => handleExtractControls(file.evidence_id)}
                    disabled={extractingEvidenceId === file.evidence_id}
                  >
                    {extractingEvidenceId === file.evidence_id
                      ? "Extracting..."
                      : "Extract controls"}
                  </button>
                </div>

                {extractions[file.evidence_id] && (
                  <div className="extraction-results">
                    <h3>Detected controls</h3>

                    {extractions[file.evidence_id].findings.length === 0 ? (
                      <p className="muted-text">
                        No supported controls were detected in this file.
                      </p>
                    ) : (
                      <ul>
                        {extractions[file.evidence_id].findings.map(
                          (finding) => (
                            <li
                              key={`${file.evidence_id}-${finding.control}`}
                            >
                              <strong>{finding.control}</strong>
                              <span>{finding.status}</span>
                              <p>{finding.evidence_text}</p>
                            </li>
                          ),
                        )}
                      </ul>
                    )}
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}