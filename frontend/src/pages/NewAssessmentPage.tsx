import {
  useState,
  type FormEvent,
  type ChangeEvent,
} from "react";
import { useNavigate } from "react-router-dom";

import { api } from "../services/api";
import type { VendorCreate } from "../types/assessment";

const initialForm: VendorCreate = {
  vendor_name: "",
  industry: "",
  data_type: "",
  hosts_pii: false,
  has_soc2: false,
  has_iso27001: false,
  mfa_enabled: false,
  encryption_at_rest: false,
  incident_response_plan: false,
  subprocessors_count: 0,
  criticality: "Low",
};

export default function NewAssessmentPage() {
  const [form, setForm] = useState<VendorCreate>(initialForm);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  function updateField<K extends keyof VendorCreate>(
    field: K,
    value: VendorCreate[K],
  ) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  function handleFileChange(
    event: ChangeEvent<HTMLInputElement>,
  ) {
    setSelectedFile(event.target.files?.[0] ?? null);
  }

async function handleSubmit(
  event: FormEvent<HTMLFormElement>,
) {
  event.preventDefault();

  setSubmitting(true);
  setError("");

  try {
    const formData = new FormData();

    formData.append(
      "vendor_data",
      JSON.stringify(form),
    );

    if (selectedFile) {
      formData.append(
        "evidence_file",
        selectedFile,
      );
    }

    await api.post(
      "/assessments/",
      formData,
    );

    navigate("/");
  } catch (requestError) {
    console.error(requestError);

    setError(
      "Could not create the assessment.",
    );
  } finally {
    setSubmitting(false);
  }
}

  return (
    <section>
      <div className="page-header">
        <h1>New Vendor Assessment</h1>
        <p>
          Enter vendor details, complete the questionnaire, and optionally
          attach supporting security documentation.
        </p>
      </div>

      <form
        className="assessment-form"
        onSubmit={handleSubmit}
      >
        <div className="form-field">
          <label htmlFor="vendor_name">Vendor name</label>
          <input
            id="vendor_name"
            required
            value={form.vendor_name}
            onChange={(event) =>
              updateField("vendor_name", event.target.value)
            }
          />
        </div>

        <div className="form-field">
          <label htmlFor="industry">Industry</label>
          <input
            id="industry"
            required
            value={form.industry}
            onChange={(event) =>
              updateField("industry", event.target.value)
            }
          />
        </div>

        <div className="form-field full-width">
          <label htmlFor="data_type">Data type</label>
          <input
            id="data_type"
            required
            value={form.data_type}
            onChange={(event) =>
              updateField("data_type", event.target.value)
            }
          />
        </div>

        <div className="form-field">
          <label htmlFor="subprocessors_count">
            Subprocessors count
          </label>

          <input
            id="subprocessors_count"
            type="number"
            min="0"
            value={form.subprocessors_count}
            onChange={(event) =>
              updateField(
                "subprocessors_count",
                Number(event.target.value),
              )
            }
          />
        </div>

        <div className="form-field">
          <label htmlFor="criticality">
            Criticality
          </label>

          <select
            id="criticality"
            value={form.criticality}
            onChange={(event) =>
              updateField(
                "criticality",
                event.target.value as VendorCreate["criticality"],
              )
            }
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
        </div>

        <div className="checkbox-grid">
          {[
            ["hosts_pii", "Hosts personally identifiable information"],
            ["has_soc2", "Has SOC 2 certification"],
            ["has_iso27001", "Has ISO 27001 certification"],
            ["mfa_enabled", "Multi-factor authentication enabled"],
            ["encryption_at_rest", "Encryption at rest enabled"],
            ["incident_response_plan", "Incident response plan available"],
          ].map(([field, label]) => (
            <label
              className="checkbox-field"
              key={field}
            >
              <input
                type="checkbox"
                checked={
                  form[field as keyof VendorCreate] as boolean
                }
                onChange={(event) =>
                  updateField(
                    field as keyof VendorCreate,
                    event.target.checked as never,
                  )
                }
              />
              {label}
            </label>
          ))}
        </div>

        {/* ---------- New Evidence Upload Section ---------- */}

        <div className="form-field full-width">
          <label htmlFor="evidence">
            Security Evidence (Optional)
          </label>

          <input
            id="evidence"
            type="file"
            accept=".txt,.pdf"
            onChange={handleFileChange}
          />

          <small className="muted-text">
            Upload SOC 2 reports, ISO 27001 certificates,
            security questionnaires, or audit reports.
          </small>

          {selectedFile && (
            <p className="muted-text">
              <strong>Selected:</strong> {selectedFile.name}
            </p>
          )}
        </div>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={submitting}
        >
          {submitting
            ? "Assessing Vendor..."
            : "Assess Vendor"}
        </button>
      </form>
    </section>
  );
}