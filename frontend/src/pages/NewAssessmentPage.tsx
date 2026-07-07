import { useState, type FormEvent } from "react";
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
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  function updateField<K extends keyof VendorCreate>(
    field: K,
    value: VendorCreate[K],
  ) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      await api.post("/assessments/", form);
      navigate("/");
    } catch (requestError) {
      console.error(requestError);
      setError("Could not create the assessment. Check that the backend is running.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section>
      <h1>New Vendor Assessment</h1>

      <form onSubmit={handleSubmit}>
        <label>
          Vendor name
          <input
            required
            value={form.vendor_name}
            onChange={(event) => updateField("vendor_name", event.target.value)}
          />
        </label>

        <label>
          Industry
          <input
            required
            value={form.industry}
            onChange={(event) => updateField("industry", event.target.value)}
          />
        </label>

        <label>
          Data type
          <input
            required
            value={form.data_type}
            onChange={(event) => updateField("data_type", event.target.value)}
          />
        </label>

        <label>
          Subprocessors count
          <input
            type="number"
            min="0"
            value={form.subprocessors_count}
            onChange={(event) =>
              updateField("subprocessors_count", Number(event.target.value))
            }
          />
        </label>

        <label>
          Criticality
          <select
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
        </label>

        {[
          ["hosts_pii", "Hosts personally identifiable information"],
          ["has_soc2", "Has SOC 2 certification"],
          ["has_iso27001", "Has ISO 27001 certification"],
          ["mfa_enabled", "Multi-factor authentication enabled"],
          ["encryption_at_rest", "Encryption at rest enabled"],
          ["incident_response_plan", "Incident response plan available"],
        ].map(([field, label]) => (
          <label key={field}>
            <input
              type="checkbox"
              checked={form[field as keyof VendorCreate] as boolean}
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

        {error && <p>{error}</p>}

        <button type="submit" disabled={submitting}>
          {submitting ? "Creating assessment..." : "Create assessment"}
        </button>
      </form>
    </section>
  );
}