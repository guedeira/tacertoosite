export function normalizeText(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

export function filterCompanies<T extends { name: string }>(companies: T[], term: string, limit = 6): T[] {
  const normalizedTerm = normalizeText(term);

  if (!normalizedTerm) {
    return [];
  }

  return companies
    .filter((company) => normalizeText(company.name).includes(normalizedTerm))
    .slice(0, limit);
}
