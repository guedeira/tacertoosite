export interface Company {
  id: string;
  name: string;
  official_domains?: string[];
}

export interface ValidationResult {
  is_match: boolean;
  company: string;
  official_domains: string[];
  submitted_domain: string;
  message: string;
}

export interface DomainValidationPayload {
  company_id: string;
  input: string;
}
