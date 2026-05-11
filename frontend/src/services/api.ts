import type { Company, DomainValidationPayload, ValidationResult } from "../types/api";

const PRODUCTION_API_BASE_URL = "https://api-tacertoosite.guedeira.dev";
const API_BASE_URL = import.meta.env.DEV
  ? "/api"
  : import.meta.env.VITE_API_BASE_URL || PRODUCTION_API_BASE_URL;

async function fetchWithTimeout(path: string, options: RequestInit = {}, timeoutInMs = 8000): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutInMs);

  try {
    return await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      signal: controller.signal,
    });
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetchWithTimeout("/health");
    return response.ok;
  } catch {
    return false;
  }
}

export async function getCompanies(): Promise<Company[]> {
  const response = await fetchWithTimeout("/companies");

  if (!response.ok) {
    throw new Error("Não foi possível carregar as empresas.");
  }

  return response.json() as Promise<Company[]>;
}

export async function validateDomain(payload: DomainValidationPayload): Promise<ValidationResult> {
  const response = await fetchWithTimeout(
    "/validate-domain",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    },
    10000,
  );

  if (!response.ok) {
    throw new Error("Não foi possível conferir o link.");
  }

  return response.json() as Promise<ValidationResult>;
}
