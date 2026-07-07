export type VendorCreate = {
  vendor_name: string;
  industry: string;
  data_type: string;
  hosts_pii: boolean;
  has_soc2: boolean;
  has_iso27001: boolean;
  mfa_enabled: boolean;
  encryption_at_rest: boolean;
  incident_response_plan: boolean;
  subprocessors_count: number;
  criticality: "Low" | "Medium" | "High";
};

export type Assessment = {
  assessment_id: string;
  risk_score: number;
  risk_tier: string;
  created_at: string;
  scoring_version: string;
  reasons: string[];
  vendor: VendorCreate & {
    vendor_id: string;
    expected_risk_tier: string;
  };
};