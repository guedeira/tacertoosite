export interface Brand {
  id: string;
  name: string;
  official_domains?: string[];
}

export interface ValidationResult {
  is_match: boolean;
  brand: string;
  official_domains: string[];
  submitted_domain: string;
  message: string;
}

export interface DomainValidationPayload {
  brand_id: string;
  input: string;
}
